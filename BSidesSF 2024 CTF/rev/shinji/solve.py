import hashlib

def md5_hash(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    return md5_hash.hexdigest()

def sha1_hash(text):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(text.encode('utf-8'))
    return sha1_hash.hexdigest()

for i in range(1577865600, 1735718401):
    if sha1_hash(md5_hash(f'shinji-{i}')) == '75b1d234851cdc94899eae8c97adce769e8ddb26':
        print(f'CTF{{{i}}}')
        break