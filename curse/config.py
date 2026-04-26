from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_ROOT / "components.db"
LOCAL_SELENIUM_ROOT = PROJECT_ROOT / ".local" / "selenium"
CHROME_CACHE_ROOT = LOCAL_SELENIUM_ROOT / "chrome" / "linux64"
CHROMEDRIVER_CACHE_ROOT = LOCAL_SELENIUM_ROOT / "chromedriver" / "linux64"

ALLOWED_TABLES = [
    "cpu",
    "motherboard",
    "ram",
    "video_card",
    "ssd",
    "hard_drive",
    "power_unit",
    "computer_case",
]

CATEGORY_LABELS = [
    "процессоры",
    "материнские платы",
    "оперативная память",
    "видеокарты",
    "твердотельные накопители (ssd)",
    "жесткие диски",
    "блоки питания",
    "корпуса",
]

SITILINK_URLS = [
    "https://www.citilink.ru/catalog/processory/?ref=mainmenu_plate&p=",
    "https://www.citilink.ru/catalog/materinskie-platy/?ref=mainmenu_plate&p=",
    "https://www.citilink.ru/catalog/moduli-pamyati/?ref=mainmenu_plate&p=",
    "https://www.citilink.ru/catalog/videokarty/?ref=mainmenu_plate&p=",
    "https://www.citilink.ru/catalog/ssd-nakopiteli/?ref=mainmenu_plate&p=",
    "https://www.citilink.ru/catalog/zhestkie-diski/?ref=mainmenu_plate&p=",
    "https://www.citilink.ru/catalog/bloki-pitaniya/?ref=mainmenu_plate&p=",
    "https://www.citilink.ru/catalog/korpusa/?ref=mainmenu_plate&p=",
]

ELDORADO_URLS = [
    "",
    "https://www.eldorado.ru/c/materinskie-platy/?page=",
    "",
    "https://www.eldorado.ru/c/videokarty/?page=",
    "https://www.eldorado.ru/c/tverdotelnye-nakopiteli-ssd/?page=",
    "",
    "https://www.eldorado.ru/c/bloki-pitaniya/?page=",
    "https://www.eldorado.ru/c/korpusa/?page=",
]
