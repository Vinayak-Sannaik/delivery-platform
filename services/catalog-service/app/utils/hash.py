import hashlib


def generate_request_hash(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()