from page_analyzer import urls_repo


def test_insert_and_find_by_id(conn):
    new_id = urls_repo.insert(conn, 'https://example.com')
    found = urls_repo.find_by_id(conn, new_id)
    assert found['name'] == 'https://example.com'


def test_find_by_name(conn):
    new_id = urls_repo.insert(conn, 'https://example.com')
    found = urls_repo.find_by_name(conn, 'https://example.com')
    assert found['id'] == new_id


def test_find_by_name_missing(conn):
    assert urls_repo.find_by_name(conn, 'https://nope.test') is None


def test_find_by_id_missing(conn):
    assert urls_repo.find_by_id(conn, 99999) is None


def test_get_all_with_last_check_no_checks(conn):
    urls_repo.insert(conn, 'https://example.com')
    rows = urls_repo.get_all_with_last_check(conn)
    assert len(rows) == 1
    assert rows[0]['last_check_at'] is None
    assert rows[0]['last_status_code'] is None


def test_get_all_with_last_check_orders_newest_first(conn):
    urls_repo.insert(conn, 'https://a.test')
    urls_repo.insert(conn, 'https://b.test')
    rows = urls_repo.get_all_with_last_check(conn)
    assert rows[0]['name'] == 'https://b.test'
    assert rows[1]['name'] == 'https://a.test'
