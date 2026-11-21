import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

def scrape_headlines(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = [h.text.strip() for h in soup.select('h1,h2')]
        return {url: headlines}
    except Exception as e:
        return {url: f'Error: {e}'}


if __name__ == "__main__":
    urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://www.github.com",
    ]
    with Pool(processes=3) as pool:
        results = pool.map(scrape_headlines, urls)
    for site_result in results:
        for site, headlines in site_result.items():
            print(f"URL: {site}\n", headlines if isinstance(headlines, list) else headlines)
            
        