import requests


def fetch_cover(url):
    return requests.get(url).content


def cache_key(book_id):
    import hashlib
    return hashlib.md5(str(book_id).encode()).hexdigest()


API_TOKEN = "s3cr3t-token-123"
