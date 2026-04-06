import requests
from bs4 import BeautifulSoup
import os
import string
from requests.exceptions import RequestException


class NatureScraper:
    def __init__(self, pages, article_type):
        self.pages = pages
        self.article_type = article_type
        self.base_url = "https://www.nature.com/nature/articles"
        self.session = requests.Session()
        self.session.headers.update({
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0"
        })

    def clean_filename(self, title):
        cleaned = ''.join(char for char in title if char not in string.punctuation)
        cleaned = cleaned.replace(" ", "_")
        return cleaned[:150]

    def safe_request(self, url, params=None):
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response
        except RequestException as e:
            print(f"[ERROR] Request failed: {url} -> {e}")
            return None

    def get_article_content(self, url):
        response = self.safe_request(url)
        if not response:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        selectors = [
            "div[itemprop='articleBody']",
            "div.c-article-body",
            "div[data-track-component='article body']"
        ]

        for selector in selectors:
            body = soup.select_one(selector)
            if body:
                paragraphs = body.find_all("p")
                text = "\n".join(p.get_text(strip=True) for p in paragraphs)
                if text:
                    return text

        teaser = soup.find("p", class_="article__teaser")
        if teaser:
            return teaser.get_text(strip=True)

        print(f"[WARN] No content found: {url}")
        return ""

    def process_page(self, page_number):
        print(f"[INFO] Processing page {page_number}")

        params = {
            "sort": "PubDate",
            "year": "2022",
            "page": page_number
        }

        response = self.safe_request(self.base_url, params=params)
        if not response:
            return

        soup = BeautifulSoup(response.text, "html.parser")

        folder_name = f"Page_{page_number}"
        os.makedirs(folder_name, exist_ok=True)

        articles = soup.find_all("article")
        if not articles:
            print(f"[WARN] No articles found on page {page_number}")
            return

        for article in articles:
            type_tag = article.find("span", {"data-test": "article.type"})
            if not type_tag:
                continue

            if type_tag.text.strip() != self.article_type:
                continue

            title_tag = article.find("a", {"data-track-action": "view article"})
            if not title_tag:
                continue

            title = title_tag.text.strip()
            article_url = "https://www.nature.com" + title_tag.get("href")

            print(f"[INFO] Fetching: {title}")

            content = self.get_article_content(article_url)
            if not content:
                continue

            filename = self.clean_filename(title) + ".txt"
            file_path = os.path.join(folder_name, filename)

            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
            except OSError as e:
                print(f"[ERROR] File write failed: {file_path} -> {e}")

    def run(self):
        for page in range(1, self.pages + 1):
            self.process_page(page)

        print("\nSaved all articles.")


def main():
    while True:
        try:
            pages = int(input("How many pages?\n> "))
            break
        except ValueError:
            print("Enter a valid number!")

    article_type = input("What article type?\n> ")

    scraper = NatureScraper(pages, article_type)
    scraper.run()


if __name__ == "__main__":
    main()