import sqlite3

from rapidfuzz import fuzz, process

from config import DATABASE_PATH


def search(category, query, limit=10, threshold=70, price=True):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {category}")
    rows = cursor.fetchall()

    names = [row['name'] for row in rows]


    matches = process.extract(query, names, scorer=fuzz.WRatio, score_cutoff=threshold)


    if not matches:
        matches = process.extract(query, names, scorer=fuzz.WRatio, score_cutoff=0)

    matched_names = set([m[0] for m in matches])
    matched_rows = [row for row in rows if row['name'] in matched_names]
    if not matched_rows:
        matched_rows = rows

    if price:
        matched_rows.sort(key=lambda r: (
            r['price'] if r['price'] is not None else float('inf'),
            -(r['rating'] if r['rating'] is not None else 0)
        ))
    else:
        matched_rows.sort(key=lambda r: (
            -(r['rating'] if r['rating'] is not None else 0),
            r['price'] if r['price'] is not None else float('inf')
        ))

    conn.close()

    ret = [dict(r) for r in matched_rows[:limit]]

    for i in ret:
        print("="*60)
        print(f"Название: {i['name']}")
        print(f"Ссылка: {i['link']}")
        print(f"Цена: {i['price']} ₽")
        print(f"Оценка: {i['rating']}")

    return ret

