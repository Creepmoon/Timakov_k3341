"""Общие функции для задачи 1."""

import os

from dotenv import load_dotenv

load_dotenv()

# По заданию: сумма от 1 до 10_000_000_000_000.
# Полный перебор на таком диапазоне занимает дни; для замеров используйте QUICK_MODE=1.
UPPER_LIMIT = 10_000_000_000_000
QUICK_LIMIT = 50_000_000

EFFECTIVE_LIMIT = QUICK_LIMIT if os.getenv("QUICK_MODE", "1") == "1" else UPPER_LIMIT
NUM_WORKERS = int(os.getenv("NUM_WORKERS", os.cpu_count() or 4))


def calculate_sum(start: int, end: int) -> int:
  """Считает сумму всех целых чисел от start до end включительно."""
  total = 0
  for i in range(start, end + 1):
    total += i
  return total


def split_range(total: int, parts: int) -> list[tuple[int, int]]:
  """Делит диапазон [1, total] на parts непересекающихся поддиапазонов."""
  chunk_size = total // parts
  ranges: list[tuple[int, int]] = []
  start = 1
  for index in range(parts):
    if index == parts - 1:
      end = total
    else:
      end = start + chunk_size - 1
    ranges.append((start, end))
    start = end + 1
  return ranges
