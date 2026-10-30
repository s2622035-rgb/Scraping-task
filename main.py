import csv
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

START_URL = "https://www.musashino-u.ac.jp/"
DOMAIN = urlparse(START_URL).netloc


sitemap = {}


visited = set()


def scrape_site(url):

    if url in visited or urlparse(url).netloc != DOMAIN:
        return

    visited.add(url)
    print(f"取得中: {url}")

    time.sleep(1)

    try:
        response = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
        )

        response.encoding = response.apparent_encoding

        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find("title")
        title_text = title_tag.get_text(strip=True) if title_tag else "No Title"

        sitemap[url] = title_text

        for a_tag in soup.find_all("a", href=True):
            next_url = urljoin(url, a_tag["href"])

            parsed_next = urlparse(next_url)
            clean_url = (
                f"{parsed_next.scheme}://{parsed_next.netloc}{parsed_next.path}"
            )

            if parsed_next.netloc == DOMAIN and clean_url not in visited:
                scrape_site(clean_url)

    except Exception as e:
        print(f"エラー発生 ({url}): {e}")


def main():
    print("スクレイピングを開始します...")
    scrape_site(START_URL)

    csv_filename = "sitemap.csv"
    with open(csv_filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Title"])  
        for url, title in sitemap.items():
            writer.writerow([url, title])

    print(f"完了しました！結果は {csv_filename} に保存されました。")


if __name__ == "__main__":
    main()