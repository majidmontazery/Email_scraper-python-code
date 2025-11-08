import sys
import re
from collections import deque
from urllib.parse import urlsplit, urljoin

import requests
from bs4 import BeautifulSoup


def main():
    user_url = input('[+] Enter Target URL to Scan: ').strip()
    if not user_url.startswith('http'):
        user_url = 'http://' + user_url

    urls = deque([user_url])
    scraped_urls = set()
    emails = set()
    max_pages = 100
    count = 0

    try:
        while urls and count < max_pages:
            count += 1
            url = urls.popleft()
            scraped_urls.add(url)

            print(f'[{count}] Processing: {url}')


            try:
                response = requests.get(url, timeout=10)
                html = response.text
            except (requests.exceptions.RequestException):
                continue


            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html, re.I))
            emails.update(new_emails)


            soup = BeautifulSoup(html, 'lxml')
            for anchor in soup.find_all('a'):
                link = anchor.get('href')
                if not link:
                    continue


                link = urljoin(url, link)


                if not link.startswith('http'):
                    continue


                if link not in urls and link not in scraped_urls:
                    urls.append(link)

    except KeyboardInterrupt:
        print('\n[!] Exiting...')
        sys.exit()


    print('\n[+] Scraping Finished')
    print(f'[+] Total Emails Found: {len(emails)}')
    for email in sorted(emails):
        print(email)


if __name__ == "__main__":
    main()
