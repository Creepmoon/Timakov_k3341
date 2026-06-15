"""Параллельный парсинг с использованием threading."""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import parse_and_save
from database import init_db
from urls import NUM_WORKERS, PARSING_URLS


def split_urls(urls: list[str], parts: int) -> list[list[str]]:
  chunk_size = max(1, len(urls) // parts)
  chunks: list[list[str]] = []
  for index in range(0, len(urls), chunk_size):
    chunks.append(urls[index : index + chunk_size])
  return chunks[:parts] if len(chunks) > parts else chunks


def main() -> None:
  init_db()
  url_chunks = split_urls(PARSING_URLS, NUM_WORKERS)
  start_time = time.perf_counter()

  with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = [
      executor.submit(parse_and_save, url)
      for chunk in url_chunks
      for url in chunk
    ]
    for future in as_completed(futures):
      future.result()

  elapsed = time.perf_counter() - start_time
  print(f"\nПодход: threading")
  print(f"URL: {len(PARSING_URLS)}, потоков: {NUM_WORKERS}")
  print(f"Время: {elapsed:.4f} с")


if __name__ == "__main__":
  main()
