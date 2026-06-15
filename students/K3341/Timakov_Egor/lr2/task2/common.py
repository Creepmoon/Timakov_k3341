"""Общие функции парсинга для задачи 2."""

import re
from html import unescape

import requests
from bs4 import BeautifulSoup
from sqlmodel import select

from database import get_session, init_db
from models import ParsedPage


def extract_title(html: str) -> str:
  soup = BeautifulSoup(html, "html.parser")
  if soup.title and soup.title.string:
    return unescape(soup.title.string.strip())
  match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
  if match:
    return unescape(re.sub(r"\s+", " ", match.group(1)).strip())
  return "Без заголовка"


def fetch_html(url: str, timeout: int = 15) -> str:
  headers = {
    "User-Agent": (
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
  }
  response = requests.get(url, timeout=timeout, headers=headers)
  response.raise_for_status()
  return response.text


def save_title(url: str, title: str) -> None:
  with get_session() as session:
    existing = session.exec(select(ParsedPage).where(ParsedPage.url == url)).first()
    if existing:
      existing.title = title
      session.add(existing)
    else:
      session.add(ParsedPage(url=url, title=title))
    session.commit()


def parse_and_save(url: str) -> str | None:
  """Загружает страницу, извлекает заголовок и сохраняет в БД."""
  try:
    html = fetch_html(url)
  except requests.RequestException as error:
    print(f"[FAIL] {url} -> {error}")
    return None

  title = extract_title(html)
  save_title(url, title)
  print(f"[OK] {url} -> {title}")
  return title
