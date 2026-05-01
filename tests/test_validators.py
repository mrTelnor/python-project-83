from page_analyzer.app import _normalize_url, _validate_url, truncate_seo


def test_validate_empty():
    assert _validate_url('') == 'URL обязателен'


def test_validate_too_long():
    assert _validate_url('a' * 256) == 'URL превышает 255 символов'


def test_validate_invalid_scheme():
    assert _validate_url('not-a-url') == 'Некорректный URL'


def test_validate_hexlet_invalid_example():
    assert _validate_url('httpsss://abcabca@test.ru') == 'Некорректный URL'


def test_validate_valid():
    assert _validate_url('https://example.com') is None


def test_normalize_strips_path_and_lowercases():
    assert _normalize_url('https://Example.COM/some/path?x=1') == 'https://example.com'


def test_truncate_seo_none():
    assert truncate_seo(None) == ''


def test_truncate_seo_empty_string():
    assert truncate_seo('') == ''


def test_truncate_seo_short():
    assert truncate_seo('short') == 'short'


def test_truncate_seo_exactly_200():
    value = 'a' * 200
    assert truncate_seo(value) == value


def test_truncate_seo_long():
    assert truncate_seo('a' * 250) == 'a' * 200 + '...'
