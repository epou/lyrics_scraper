from urllib.parse import urlparse
import re


def is_url(url):
    """Check if the parameters is an url or not."""
    # Returns True if it's an url, False either.
    result = urlparse(url=url)
    return all([result.scheme, result.netloc])


def clean_text(text):
    """Clean a text."""
    # Remove all charaters that are not letters, spaces, digits or '.
    text = re.sub(r'[^A-Za-z\s\d\']', '', text)
    # Remove \n, \t and \r
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\r', ' ')
    # Remove alone characters
    text = re.sub(r' +. +', ' ', text)
    # Remove multiple spaces
    test = re.sub(r' +', ' ', text)
    # Strip spaces from left and right
    text = text.strip()
    return text
