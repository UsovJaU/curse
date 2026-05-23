import eldorado as eld
import sitilink as sit
import search as sea

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

allowed_tables = ["cpu", "motherboard", "ram", "video_card", "ssd", "hard_drive", "power_unit", "computer_case"]

from concurrent.futures import ThreadPoolExecutor

def run_eldorado(inp):
    try:
        eld.parse(ELDORADO_URLS[inp], allowed_tables[inp], "https://www.eldorado.ru")
    except:
        print("Парсер Эльдорадо упал, возможно антибот вас забанил, попробуйте позже или используйте прокси")
    

def run_citilink(inp):
    try:
        sit.parse(SITILINK_URLS[inp], allowed_tables[inp], "https://www.citilink.ru")
    except:
        print("Парсер Ситилинк упал, возможно антибот вас забанил, попробуйте позже или используйте прокси")

def main():
    print("Выберите категорию: \n1 - процессоры\n2 - материнские платы\n3 - оперативная память\n4 - видеокарты\n5 - ssd\n6 - жесткие диски\n7 - блоки питания\n8 - корпуса")
    inp = int(input()) - 1
    print("Хотите ли обновить базы данных? (yes для подтвержения)")
    obn = input().lower()
    if obn == "yes":
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_eld = executor.submit(run_eldorado, inp)
            future_sit = executor.submit(run_citilink, inp)

            future_eld.result()
            future_sit.result()

main()
