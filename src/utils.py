import hashlib

def to_SHA256(*args):
    sha256_hash = hashlib.sha256()

    for item in args:
        sha256_hash.update(item)

    return sha256_hash.digest()