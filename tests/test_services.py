from services import get_domain_from_url


def test_get_domain_from_valid_urls():
    assert get_domain_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "youtube.com"
    assert get_domain_from_url("https://youtu.be/dQw4w9WgXcQ") == "youtu.be"
    assert get_domain_from_url("https://www.tiktok.com/@user/video/123") == "tiktok.com"
    assert get_domain_from_url("https://vm.tiktok.com/ZM8ABC123/") == "vm.tiktok.com"
    assert get_domain_from_url("https://instagram.com/p/Cxyz123") == "instagram.com"


def test_get_domain_with_ports():
    assert get_domain_from_url("http://localhost:8000/test") == "localhost"
    assert get_domain_from_url("https://example.com:443/page") == "example.com"


def test_get_domain_invalid_or_non_http():
    assert get_domain_from_url("ftp://example.com/file") is None
    assert get_domain_from_url("not_a_url") is None
    assert get_domain_from_url("") is None
    assert get_domain_from_url("http://") is None
