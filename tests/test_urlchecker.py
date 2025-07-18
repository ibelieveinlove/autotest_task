
import pytest
from fileworker import url_checker

@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://ya.ru", True),
        ("http://example.com/path", True),
        ("ftp://example.com", False),       # неподдерживаемый протокол
        ("htttp://typo.com", False),        # опечатка в схеме
        ("", False)                         # пустая строка
    ],
)
def test_url_checker(url, expected):
    assert url_checker(url) is expected