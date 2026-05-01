from page_analyzer import checks_repo, urls_repo


def test_insert_full_fields(conn):
    url_id = urls_repo.insert(conn, 'https://example.com')
    check_id = checks_repo.insert(
        conn,
        url_id,
        status_code=200,
        h1='Hello',
        title='World',
        description='Desc',
    )
    rows = checks_repo.get_by_url_id(conn, url_id)
    assert len(rows) == 1
    assert rows[0]['id'] == check_id
    assert rows[0]['status_code'] == 200
    assert rows[0]['h1'] == 'Hello'
    assert rows[0]['title'] == 'World'
    assert rows[0]['description'] == 'Desc'


def test_insert_minimal_fields(conn):
    url_id = urls_repo.insert(conn, 'https://example.com')
    checks_repo.insert(conn, url_id)
    rows = checks_repo.get_by_url_id(conn, url_id)
    assert rows[0]['status_code'] is None
    assert rows[0]['h1'] is None
    assert rows[0]['title'] is None
    assert rows[0]['description'] is None


def test_get_by_url_id_orders_newest_first(conn):
    url_id = urls_repo.insert(conn, 'https://example.com')
    first = checks_repo.insert(conn, url_id)
    second = checks_repo.insert(conn, url_id)
    rows = checks_repo.get_by_url_id(conn, url_id)
    assert rows[0]['id'] == second
    assert rows[1]['id'] == first


def test_get_by_url_id_empty(conn):
    url_id = urls_repo.insert(conn, 'https://example.com')
    assert checks_repo.get_by_url_id(conn, url_id) == []
