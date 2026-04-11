import requests
from bs4 import BeautifulSoup
import string
from pathlib import Path
from requests.exceptions import RequestException


class DataCollector:
    def __init__(self, depth, category):
        self.depth = depth
        self.category = category
        self.root_url = "https://www.nature.com/nature/articles"
        self.worker = requests.Session()
        # Обновили User-Agent на более детальный
        self.worker.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-GB,en;q=0.9"
        })

    def _format_name(self, raw_title):
        """Очистка заголовка для создания имени файла."""
        valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
        clean = ''.join(c for c in raw_title if c in valid_chars)
        return clean.replace(" ", "_").strip()[:120]

    def _fetch_page(self, link, query=None):
        """Безопасное выполнение HTTP-запроса."""
        try:
            resp = self.worker.get(link, params=query, timeout=15)
            resp.raise_for_status()
            return resp
        except RequestException as err:
            print(f"--- Сбой при обращении к {link}: {err}")
            return None

    def _extract_body(self, full_url):
        """Поиск текстового содержимого статьи."""
        resp = self._fetch_page(full_url)
        if not resp:
            return ""

        parser = BeautifulSoup(resp.text, "html.parser")

        # Список вероятных контейнеров контента
        containers = [
            "article.c-article-body",
            "div.main-content",
            "div[itemprop='articleBody']",
            "div.article-item__body"
        ]

        for css_selector in containers:
            element = parser.select_one(css_selector)
            if element:
                nodes = element.find_all("p")
                result_text = "\n".join(node.get_text(strip=True) for node in nodes)
                if result_text.strip():
                    return result_text

        # Запасной вариант - краткое описание
        snippet = parser.find("p", class_="article__teaser")
        return snippet.get_text(strip=True) if snippet else ""

    def _handle_pagination(self, idx):
        print(f"[*] Анализ страницы №{idx}...")

        query_data = {
            "sort": "PubDate",
            "year": "2022",
            "page": idx
        }

        resp = self._fetch_page(self.root_url, query=query_data)
        if not resp:
            return

        soup = BeautifulSoup(resp.text, "html.parser")

        # Создание директории через pathlib
        target_dir = Path(f"Page_{idx}")
        target_dir.mkdir(exist_ok=True)

        items = soup.find_all("article")
        if not items:
            print(f"[-] На странице {idx} ничего не найдено.")
            return

        for entry in items:
            # Проверка типа статьи
            label = entry.find("span", {"data-test": "article.type"})
            if not label or label.text.strip() != self.category:
                continue

            link_node = entry.find("a", {"data-track-action": "view article"})
            if not link_node:
                continue

            article_name = link_node.text.strip()
            path_suffix = link_node.get("href")
            full_path = f"https://www.nature.com{path_suffix}"

            print(f"    -> Загрузка: {article_name[:50]}...")

            body_text = self._extract_body(full_path)
            if not body_text:
                continue

            file_identity = self._format_name(article_name) + ".txt"
            final_dest = target_dir / file_identity

            try:
                final_dest.write_text(body_text, encoding="utf-8")
            except Exception as e:
                print(f"!!! Ошибка записи {file_identity}: {e}")

    def launch(self):
        for i in range(1, self.depth + 1):
            self._handle_pagination(i)
        print("\nПроцесс сбора данных завершен.")


def start_interactive():
    while True:
        try:
            p_count = int(input("Введите глубину поиска (кол-во страниц):\n> "))
            if p_count > 0:
                break
        except ValueError:
            pass
        print("Ошибка: введите положительное число.")

    target_type = input("Введите категорию статей (например, Research Highlight):\n> ").strip()

    app = DataCollector(p_count, target_type)
    app.launch()


if __name__ == "__main__":
    start_interactive()