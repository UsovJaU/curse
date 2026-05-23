from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
import re
from bs4 import BeautifulSoup
import sqlite3
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
    products = soup.find_all('div', class_=re.compile(r'SnippetProductVerticalLayout'))

    data = []

    for product in products:
        # Название
        title_tag = product.find('a', title=True)
        name = title_tag['title'] if title_tag and title_tag.get('title') else None

        # Ссылка на товар
        link_tag = product.find('a', href=True)
        if link_tag and link_tag.get('href'):
            url = link_tag['href']
            if url.startswith('/'):
                url = site + url
        else:
            url = None

        # Цена
        price_tag = product.find('span', class_=re.compile(r'MainPriceNumber'))
        if price_tag:
            price = price_tag.get_text(strip=True).replace(' ', '')
        else:
            price_meta = product.find(attrs={'data-meta-price': True})
            price = price_meta['data-meta-price'] if price_meta else None

        # Оценка
        rating_tag = product.find('div', attrs={'data-meta-name': 'MetaInfo_rating'})
        if rating_tag:
            rating_text = rating_tag.get_text(strip=True)
            match = re.search(r'(\d+\.?\d*)', rating_text)
            rating = match.group(1) if match else None
        else:
            rating = None

        if name:
            data.append((url, name, price, rating))

    return data


    
def parse(url, name, site):
    if not url:
        return False
    options = Options()
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

    # --- Selenium часть (НЕ ТРОГАЕМ ЛОГИКУ) ---
    driver.get(site)
    time.sleep(random.uniform(2, 4))
    #url = "https://www.citilink.ru/catalog/processory/?ref=mainmenu_plate&p="
    page = 1
    allowed_tables = {"cpu", "motherboard", "ram", "video_card", "ssd", "hard_drive", "power_unit", "computer_case"}
    if name not in allowed_tables:
        raise ValueError("Недопустимое имя таблицы!")
    while True:
    
        l_url = f"{url}{page}"
        count = 0
        driver.get(l_url)
        for _ in range(5):
            driver.execute_script("window.scrollBy(0, arguments[0]);", random.randint(300, 800))
            time.sleep(random.uniform(0.5, 1.5))
            time.sleep(random.uniform(3, 5))
        html = driver.page_source
        products = extract_products_from_html(html, site)
        print(f"Найдено товаров: {len(products)}")
        with sqlite3.connect('components.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name} (link TEXT PRIMARY KEY, name TEXT NOT NULL, price INTEGER NOT NULL, rating REAL NOT NULL)""")
            for product in products:
                try:
                    cursor.execute(f"""INSERT INTO {name} (link, name, price, rating)VALUES (?, ?, ?, ?)""", product)
                    count += 1
                    print("writed!")
                except:
                    cursor.execute(f"""SELECT 1 FROM {name} WHERE link = ? LIMIT 1""", (product[0],))
                    exists = cursor.fetchone()
                    if exists:
                        try:
                            cursor.execute(f"""UPDATE {name} SET name = ?, price = ?, rating = ? WHERE link = ?""", (product[1], product[2], product[3], product[0]))
                            print("changed!")
                            count += 1
                        except:
                            pass
                    
        if count:
            page += 1
        else:
            break
    driver.quit()

#parse("https://www.citilink.ru/catalog/processory/?ref=mainmenu_plate&p=", "cpu", https://www.citilink.ru/)
