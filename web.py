import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    return response.text

def scrape_pages(base_url, num_pages):
    data = []
    for page in range(1, num_pages + 1):
        print(f"Scraping page: {page}")
        url = f"{base_url}/page/{page}/"
        try:
            html = get_html(url)
            soup = BeautifulSoup(html, 'html.parser')
            quotes = soup.find_all('div', class_='quote')
            for quote in quotes:
                text = quote.find('span', class_='text').get_text(strip=True)
                author = quote.find('small', class_='author').get_text(strip=True)
                tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
                data.append({'text': text, 'author': author, 'tags': ', '.join(tags)})
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data from page {page}: {e}")
    return data

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['text', 'author', 'tags'])
        writer.writeheader()
        writer.writerows(data)

def main():
    base_url = 'http://quotes.toscrape.com/'
    num_pages_to_scrape = 5
    scraped_data = scrape_pages(base_url, num_pages_to_scrape)
    print("Scraped data:", scraped_data)
    save_to_csv(scraped_data, 'quotes.csv')

if __name__ == "__main__":
    main()
