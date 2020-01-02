import hashlib


def get_md5(string):
    code_url = string.encode("utf-8")
    m = hashlib.md5()
    m.update(code_url)
    return m.hexdigest()


if __name__ == '__main__':
   pass
