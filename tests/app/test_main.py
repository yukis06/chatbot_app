from app.main import get_content


def test_get_content() -> None:
    url = "https://gridpredict.jp/"
    content = get_content(url)
    assert isinstance(content, str)