import sqlite3
from rapidfuzz import fuzz, process

def search(category, query, limit=10, threshold=70, price=True):
    db_path = 'components.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {category}")
    rows = cursor.fetchall()

    names = [row['name'] for row in rows]

    # 1. основной поиск
    matches = process.extract(query, names, scorer=fuzz.WRatio, score_cutoff=threshold)

    # 2. если ничего не нашли — ослабляем поиск
    if not matches:
        matches = process.extract(query, names, scorer=fuzz.WRatio, score_cutoff=0)

    matched_names = set([m[0] for m in matches])
    matched_rows = [row for row in rows if row['name'] in matched_names]
    f = False
    # 3. если вообще пусто — берём просто все
    if not matched_rows:
        matched_rows = rows
        f = True

    # 4. сортировка
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

# Пример использования:
#results = search('video_card', '')
#print(results)
