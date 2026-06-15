"""Подсчёт суммы с использованием threading."""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import EFFECTIVE_LIMIT, NUM_WORKERS, calculate_sum, split_range


def main() -> None:
  ranges = split_range(EFFECTIVE_LIMIT, NUM_WORKERS)
  start_time = time.perf_counter()

  total = 0
  with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = [executor.submit(calculate_sum, start, end) for start, end in ranges]
    for future in as_completed(futures):
      total += future.result()

  elapsed = time.perf_counter() - start_time
  expected = EFFECTIVE_LIMIT * (EFFECTIVE_LIMIT + 1) // 2

  print(f"Подход: threading")
  print(f"Диапазон: 1 .. {EFFECTIVE_LIMIT:,}")
  print(f"Число потоков: {NUM_WORKERS}")
  print(f"Результат: {total}")
  print(f"Ожидаемое: {expected}")
  print(f"Время: {elapsed:.4f} с")


if __name__ == "__main__":
  main()
