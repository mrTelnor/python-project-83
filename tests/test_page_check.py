import pytest
import requests
import responses

from page_analyzer.page_check import fetch_page_data


@responses.activate
def test_fetch_full_html():
    html = '''
    <html><head>
        <title>Awesome page</title>
        <meta name="description" content="Statements of great people">
    </head><body>
        <h1>Do not expect a miracle, miracles yourself!</h1>
    </body></html>
    '''
    responses.add(responses.GET, 'http://example.com', body=html, status=200)
    data = fetch_page_data('http://example.com')
    assert data['status_code'] == 200
    assert data['h1'] == 'Do not expect a miracle, miracles yourself!'
    assert data['title'] == 'Awesome page'
    assert data['description'] == 'Statements of great people'


@responses.activate
def test_fetch_html_without_seo_tags():
    responses.add(
        responses.GET, 'http://example.com',
        body='<html></html>', status=200,
    )
    data = fetch_page_data('http://example.com')
    assert data['status_code'] == 200
    assert data['h1'] is None
    assert data['title'] is None
    assert data['description'] is None


@responses.activate
def test_fetch_404_raises():
    responses.add(responses.GET, 'http://example.com', body='', status=404)
    with pytest.raises(requests.HTTPError):
        fetch_page_data('http://example.com')


@responses.activate
def test_fetch_500_raises():
    responses.add(responses.GET, 'http://example.com', body='', status=500)
    with pytest.raises(requests.HTTPError):
        fetch_page_data('http://example.com')


@responses.activate
def test_fetch_connection_error():
    responses.add(
        responses.GET, 'http://example.com',
        body=requests.ConnectionError('boom'),
    )
    with pytest.raises(requests.ConnectionError):
        fetch_page_data('http://example.com')


@responses.activate
def test_fetch_utf8_without_charset_header():
    html = (
        '<html><head><meta charset="utf-8">'
        '<title>Привет</title></head></html>'
    )
    responses.add(
        responses.GET, 'http://example.com',
        body=html.encode('utf-8'),
        status=200,
        content_type='text/html',
    )
    data = fetch_page_data('http://example.com')
    assert data['title'] == 'Привет'
