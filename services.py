from urllib.parse import urlparse

SERVICE_DOMAINS = {
    "youtube": ("youtube.com", "youtu.be"),
    "tiktok": ("tiktok.com", "vm.tiktok.com", "vt.tiktok.com"),
    "instagram": ("instagram.com", "instagr.am"),
}


def get_domain_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    if not parsed.netloc:
        return None
    if parsed.scheme not in ("http", "https"):
        return None
    domain_parts = parsed.netloc.removeprefix("www.").split(':')[0].lower()
    return domain_parts
