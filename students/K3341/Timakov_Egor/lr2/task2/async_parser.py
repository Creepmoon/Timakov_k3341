"""Параллельный парсинг с использованием asyncio и aiohttp."""

import asyncio
import re
import time
from html import unescape

import aiohttp
from bs4 import BeautifulSoup
from sqlmodel import select

from database import get_session, init_db
from models import ParsedPage
from urls import PARSING_URLS

HEADERS = {
  "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  ),
  "Accept": "text/html,application/xhtml+xml",
}


def extract_title(html: str) -> str:
  soup = BeautifulSoup(html, "html.parser")
  if soup.title and soup.title.string:
    return unescape(soup.title.string.strip())
  match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
  if match:
    return unescape(re.sub(r"\s+", " ", match.group(1)).strip())
  return "Без заголовка"


def save_title(url: str, title: str) -> None:
  with get_session() as session:
    existing = session.exec(select(ParsedPage).where(ParsedPage.url == url)).first()
    if existing:
      existing.title = title
      session.add(existing)
    else:
      session.add(ParsedPage(url=url, title=title))
    session.commit()


async def parse_and_save(session: aiohttp.ClientSession, url: str) -> str | None:
  """Загружает страницу, извлекает заголовок и сохраняет в БД."""
  try:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
      response.raise_for_status()
      html = await response.text()
  except (aiohttp.ClientError, asyncio.TimeoutError) as error:
    print(f"[FAIL] {url} -> {error}")
    return None

  title = extract_title(html)
  await asyncio.to_thread(save_title, url, title)
  print(f"[OK] {url} -> {title}")
  return title


async def main_async() -> float:
  init_db()
  start_time = time.perf_counter()
  async with aiohttp.ClientSession(headers=HEADERS) as session:
    await asyncio.gather(*(parse_and_save(session, url) for url in PARSING_URLS))
  return time.perf_counter() - start_time


def main() -> None:
  elapsed = asyncio.run(main_async())
  print(f"\nПодход: asyncio + aiohttp")
  print(f"URL: {len(PARSING_URLS)}")
  print(f"Время: {elapsed:.4f} с")


if __name__ == "__main__":
  main()
