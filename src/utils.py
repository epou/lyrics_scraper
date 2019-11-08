from urllib.parse import urlparse
import re

def is_url(url):
    result = urlparse(url=url)
    return all([result.scheme, result.netloc])

def clean_text(text):
    text = re.sub(r'[^A-Za-z\s\d\']', '', text)
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\r', ' ')
    text = re.sub(r' +. +', ' ', text)
    test = re.sub(r' +', ' ', text)
    text = text.strip()
    return text
