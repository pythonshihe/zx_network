import re


def deal_str(txt):
    if txt:
        string = re.sub("\n|\r|\s|\t", "", txt[0])
    else:
        string = ''
    return string
