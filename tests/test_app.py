import responses


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Анализатор страниц' in response.get_data(as_text=True)


def test_create_url_valid(client):
    response = client.post('/urls', data={'url': 'https://example.com'})
    assert response.status_code == 302
    assert response.location.startswith('/urls/')


def test_create_url_invalid_returns_422(client):
    response = client.post('/urls', data={'url': 'httpsss://abcabca@test.ru'})
    assert response.status_code == 422
    assert 'Некорректный URL' in response.get_data(as_text=True)


def test_create_url_duplicate_redirects_to_existing(client):
    first = client.post('/urls', data={'url': 'https://example.com'})
    second = client.post('/urls', data={'url': 'https://example.com'})
    assert first.location == second.location


def test_urls_list_shows_added(client):
    client.post('/urls', data={'url': 'https://example.com'})
    response = client.get('/urls')
    assert response.status_code == 200
    assert 'https://example.com' in response.get_data(as_text=True)


def test_url_show_missing_returns_404(client):
    response = client.get('/urls/99999')
    assert response.status_code == 404


@responses.activate
def test_check_creates_record_on_success(client):
    client.post('/urls', data={'url': 'https://example.com'})
    responses.add(
        responses.GET, 'https://example.com',
        body='<html><h1>Hi</h1></html>', status=200,
    )
    response = client.post('/urls/1/checks')
    assert response.status_code == 302
    show = client.get('/urls/1')
    assert b'200' in show.data


@responses.activate
def test_check_does_not_create_record_on_error(client):
    client.post('/urls', data={'url': 'https://example.com'})
    responses.add(responses.GET, 'https://example.com', body='', status=500)
    response = client.post('/urls/1/checks')
    assert response.status_code == 302
    show = client.get('/urls/1')
    assert 'Произошла ошибка при проверке' in show.get_data(as_text=True)
