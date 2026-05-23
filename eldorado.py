from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import re
from bs4 import BeautifulSoup
import sqlite3
import json
from bs4 import BeautifulSoup
from pathlib import Path


CHROME_CACHE_ROOT = Path("/home/admen/.cache/selenium/chrome/linux64")
CHROMEDRIVER_CACHE_ROOT = Path("/home/admen/.cache/selenium/chromedriver/linux64")


def create_chrome_driver(options):
    for version_dir in sorted(CHROME_CACHE_ROOT.iterdir(), reverse=True):
        chrome_binary = version_dir / "chrome"
        chromedriver_binary = CHROMEDRIVER_CACHE_ROOT / version_dir.name / "chromedriver"
        if (
            version_dir.is_dir()
            and chrome_binary.exists()
            and chromedriver_binary.exists()
            and not (version_dir / "sm.lock").exists()
        ):
            options.binary_location = str(chrome_binary)
            service = Service(executable_path=str(chromedriver_binary))
            return webdriver.Chrome(service=service, options=options)

    raise RuntimeError("Не найдена завершённая совпадающая пара chrome/chromedriver в кеше Selenium.")




# --- ПАРСИНГ ФУНКЦИЯ ---
def extract_products_from_html(html, site):
    soup = BeautifulSoup(html, 'html.parser')

    script = soup.find('script', id="__NEXT_DATA__")
    if not script:
        return []

    data = json.loads(script.string)

    # ID текущей категории
    target_category = data["props"]["initialState"]["listing-module"]["virtualCategoryId"]

    # Все товары
    all_products = data["props"]["initialState"]["products-store-module"]["products"]

    result = []

    for product in all_products.items():
        # Пропускаем всё, что не из нужной категории
        if product.get("categoryId") != target_category:
            continue

        name = product.get("name")
        code = product.get("code")
        url = f"{site}/cat/detail/{code}/" if code else None
        price = product.get("price")
        rating = product.get("rating")

        if name:
            result.append((url, name, price, rating))

    return result

def parse(url, name, site):
    if not url:
        return False

    options = Options()
    #options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )

    driver = create_chrome_driver(options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    #driver.get(site)
    #time.sleep(random.uniform(2, 4))

    page = 1
    f = True

    allowed_tables = {
        "cpu", "motherboard", "ram", "video_card",
        "ssd", "hard_drive", "power_unit", "computer_case"
    }
    if name not in allowed_tables:
        raise ValueError("Недопустимое имя таблицы!")

    while True:
        l_url = f"{url}{page}"
        count = 0

        driver.get(l_url)
        
        # Ждём появления товаров (максимум 10 секунд)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "__NEXT_DATA__")))
        except:
            # Если товаров нет за 10 секунд - считаем что страница пустая
            print(f"Товары не загрузились на странице {page}")
            break
        time.sleep(5)
        '''for _ in range(5):
            driver.execute_script(
                "window.scrollBy(0, arguments[0]);",
                random.randint(300, 800)
            )
            time.sleep(random.uniform(0.5, 1.5))
            time.sleep(random.uniform(3, 5))'''

        html = driver.page_source
        current_url = driver.current_url
        if current_url == url[:-6] and page != 1:
            break
        products = extract_products_from_html(html, site)

        print(f"Найдено товаров: {len(products)}")

        with sqlite3.connect('components.db') as conn:
            cursor = conn.cursor()

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    link TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    rating REAL NOT NULL
                )
            """)

            for product in products:
                try:
                    cursor.execute(f"""
                        INSERT INTO {name} (link, name, price, rating)
                        VALUES (?, ?, ?, ?)
                    """, product)
                    count += 1
                    print("el writed!")

                except:
                    cursor.execute(
                        f"SELECT 1 FROM {name} WHERE link = ? LIMIT 1",
                        (product[0],)
                    )
                    exists = cursor.fetchone()

                    if exists:
                        try:
                            cursor.execute(f"""
                                UPDATE {name}
                                SET name = ?, price = ?, rating = ?
                                WHERE link = ?
                            """, (
                                product[1],
                                product[2],
                                product[3],
                                product[0]
                            ))

                            print("changed!")
                            count += 1

                            if f:
                                f = False
                                buf = product
                            elif buf == product:
                                break

                        except:
                            pass

        if count:
            page += 1
            
        else:
            break

    driver.quit()

'''allowed_tables = ["cpu", "motherboard", "ram", "video_card", "ssd", "hard_drive", "power_unit", "computer_case"]
eldorado=["", "https://www.eldorado.ru/c/materinskie-platy/?page=", "https://www.eldorado.ru/c/videokarty/?page="]
inp = 2
parse(eldorado[inp], allowed_tables[inp], "https://www.eldorado.ru")'''
