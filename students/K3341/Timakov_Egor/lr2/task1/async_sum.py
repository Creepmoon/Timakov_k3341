"""Подсчёт суммы с использованием asyncio."""

import asyncio
import time

from common import EFFECTIVE_LIMIT, NUM_WORKERS, calculate_sum, split_range


async def calculate_sum_async(start: int, end: int) -> int:
  return calculate_sum(start, end)


async def main_async() -> tuple[int, float]:
  ranges = split_range(EFFECTIVE_LIMIT, NUM_WORKERS)
  start_time = time.perf_counter()

  tasks = [asyncio.create_task(calculate_sum_async(start, end)) for start, end in ranges]
  results = await asyncio.gather(*tasks)

  elapsed = time.perf_counter() - start_time
  return sum(results), elapsed


def main() -> None:
  total, elapsed = asyncio.run(main_async())
  expected = EFFECTIVE_LIMIT * (EFFECTIVE_LIMIT + 1) // 2

  print(f"Подход: asyncio")
  print(f"Диапазон: 1 .. {EFFECTIVE_LIMIT:,}")
  print(f"Число задач: {NUM_WORKERS}")
  print(f"Результат: {total}")
  print(f"Ожидаемое: {expected}")
  print(f"Время: {elapsed:.4f} с")


if __name__ == "__main__":
  main()
