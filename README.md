# curse

Локальный CLI для обновления базы комплектующих и поиска по ней.

## Запуск

Через локальный launcher:

```bash
./curse "Intel Core i3 12100" --category 1 --sort price
```

С обновлением базы перед поиском:

```bash
./curse "RTX 4060" --category 4 --sort rating --update
```

Интерактивный режим:

```bash
./curse
```

## Установка console script в `.venv`

```bash
.venv/bin/pip install -e .
```

После этого команда будет доступна как:

```bash
.venv/bin/curse "Kingston SSD" --category 5
```
