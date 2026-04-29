import requests

REQUEST_TIMEOUT = 5


def fetch_page_data(url):
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return {
        'status_code': response.status_code,
    }
