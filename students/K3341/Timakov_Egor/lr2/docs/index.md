# Лабораторная работа 2

**Тема:** потоки, процессы и асинхронность в Python.

Цель работы — понять отличия между `threading`, `multiprocessing` и `asyncio`, а также научиться выбирать подходящий инструмент для CPU-bound и I/O-bound задач.

## Задачи

| № | Описание | Тип нагрузки |
|---|----------|--------------|
| [Задача 1](task1.md) | Параллельный подсчёт суммы чисел от 1 до N | CPU-bound |
| [Задача 2](task2.md) | Параллельный парсинг веб-страниц с сохранением в БД | I/O-bound |

Для каждой задачи реализованы **три варианта** программы:

- `threading` — потоки в одном процессе
- `multiprocessing` — отдельные процессы
- `asyncio` — кооперативная асинхронность (`async`/`await`)

## Структура проекта

```
lr2/
├── task1/
│   ├── common.py
│   ├── threading_sum.py
│   ├── multiprocessing_sum.py
│   └── async_sum.py
├── task2/
│   ├── models.py
│   ├── database.py
│   ├── common.py
│   ├── urls.py
│   ├── threading_parser.py
│   ├── multiprocessing_parser.py
│   └── async_parser.py
├── docs/              # документация MkDocs
├── mkdocs.yml
├── requirements.txt
└── README.md
```

## Быстрый старт

```bash
cd lr2
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # Windows
```

Запуск программ:

```bash
cd task1 && python threading_sum.py
cd task2 && python async_parser.py
```

Просмотр документации:

```bash
mkdocs serve
```

Сайт откроется по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Содержание документации

- [Установка и настройка](setup.md)
- [Задача 1 — подсчёт суммы](task1.md)
- [Задача 2 — парсинг веб-страниц](task2.md)
- [Замеры и сравнение результатов](benchmarks.md)
- [Теоретические материалы](theory.md)

## Автор

Тимаков Егор, группа K3341, ИТМО, 2026
