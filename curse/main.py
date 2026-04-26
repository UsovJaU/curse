import argparse

import eldorado as eld
import search as sea
import sitilink as sit
from config import ALLOWED_TABLES, CATEGORY_LABELS, ELDORADO_URLS, SITILINK_URLS


def build_parser():
    parser = argparse.ArgumentParser(
        prog="curse",
        description="Поиск комплектующих с опциональным обновлением локальной базы.",
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="Поисковый запрос, например: Intel Core i3 12100",
    )
    parser.add_argument(
        "-c",
        "--category",
        type=int,
        choices=range(1, len(ALLOWED_TABLES) + 1),
        help="Номер категории из списка.",
    )
    parser.add_argument(
        "--sort",
        choices=("price", "rating"),
        default="price",
        help="Сортировка результатов.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Обновить локальную базу перед поиском.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Сколько результатов показать.",
    )
    return parser


def print_categories():
    for index, label in enumerate(CATEGORY_LABELS, start=1):
        print(f"{index} - {label}")


def prompt_category():
    while True:
        print_categories()
        raw = input("Введите номер категории: ").strip()
        if raw.isdigit():
            index = int(raw)
            if 1 <= index <= len(ALLOWED_TABLES):
                return index
        print("Неверный номер категории, попробуйте ещё раз.")


def prompt_update():
    while True:
        raw = input("Обновить базы перед поиском? (yes/no): ").strip().lower()
        if raw in {"yes", "y"}:
            return True
        if raw in {"no", "n", ""}:
            return False
        print("Введите yes или no.")


def prompt_sort():
    while True:
        raw = input("Сортировка: 1 - по цене, 2 - по оценке: ").strip()
        if raw == "1":
            return "price"
        if raw == "2":
            return "rating"
        print("Введите 1 или 2.")


def prompt_query():
    while True:
        raw = input("Введите запрос, например Intel Core i3 12100: ").strip()
        if raw:
            return raw
        print("Запрос не должен быть пустым.")


def update_sources(category_index):
    table_name = ALLOWED_TABLES[category_index]
    sit.parse(SITILINK_URLS[category_index], table_name, "https://www.citilink.ru")
    eld.parse(ELDORADO_URLS[category_index], table_name, "https://www.eldorado.ru")


def run(query, category_number, sort_mode, update, limit):
    category_index = category_number - 1
    table_name = ALLOWED_TABLES[category_index]

    if update:
        update_sources(category_index)

    return sea.search(
        table_name,
        query,
        limit=limit,
        price=(sort_mode == "price"),
    )


def interactive_run():
    category_number = prompt_category()
    update = prompt_update()
    sort_mode = prompt_sort()
    query = prompt_query()
    run(query, category_number, sort_mode, update, limit=10)


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.query and args.category:
        run(args.query, args.category, args.sort, args.update, args.limit)
        return

    interactive_run()


if __name__ == "__main__":
    main()
