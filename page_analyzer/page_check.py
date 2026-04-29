import requests
from bs4 import BeautifulSoup

REQUEST_TIMEOUT = 5


def fetch_page_data(url):
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    return {
        'status_code': response.status_code,
        'h1': _extract_h1(soup),
        'title': _extract_title(soup),
        'description': _extract_description(soup),
    }


def _extract_h1(soup):
    tag = soup.find('h1')
    return tag.get_text(strip=True) if tag else None


def _extract_title(soup):
    tag = soup.find('title')
    return tag.get_text(strip=True) if tag else None


def _extract_description(soup):
    tag = soup.find('meta', attrs={'name': 'description'})
    return tag.get('content') if tag else None
