from urllib import parse
from abc import ABC, abstractmethod
import requests as r
from requests.exceptions import HTTPError
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from bs4.element import Comment
import re

import datetime

from .exceptions import ArtistNotFound, SongNotFound
from .utils import is_url, clean_text
from .models import Song, Artist, Album

class Base(ABC):

    ALLOWED_ITERABLE_INPUT = (list, tuple)
    ALLOWED_NON_ITERABLE_INPUT = (str)

    PAGE_URL = "https://www.azlyrics.com/"

    @classmethod
    def build_url(cls, *args, **kwargs):
        return parse.urljoin(
            base=cls.PAGE_URL,
            url=cls.build_url_path(*args, **kwargs)
        )

    @classmethod
    @abstractmethod
    def build_url_path(cls, *args, **kwargs):
        raise NotImplementedError()

    def __init__(self, url_or_name):
        url = None
        if isinstance(url_or_name, self.ALLOWED_ITERABLE_INPUT):
            url = self.build_url(*url_or_name)
        elif isinstance(url_or_name, self.ALLOWED_NON_ITERABLE_INPUT):
            url = url_or_name if is_url(url_or_name) else self.build_url(url_or_name)

        self.url = url

    @classmethod
    def _do_request(cls, url):
        headers = {'User-Agent': UserAgent().random}
        return r.get(url=url, headers=headers)

    @classmethod
    def _check_response(cls, response):
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == r.codes.not_found:
                exception = cls.exception_404_error()
                raise exception from None
            else:
                raise

    @abstractmethod
    def exception_404_error(self):
        raise NotImplementedError()

    @classmethod
    def get_bs4(cls, url, features='html.parser', remove_taglist=None):
        response = cls._do_request(url=url)
        cls._check_response(response=response)
        soup = BeautifulSoup(
            markup=response.text,
            features=features
        )

        cls._clean_soup(soup=soup, taglist=remove_taglist)
        return soup

    @classmethod
    def _clean_soup(cls, soup, taglist=None):
        _ = [x.extract() for x in soup(taglist)] if taglist else None
        _ = [x.extract() for x in soup.find_all(text=lambda text: isinstance(text, Comment))]

    def run(self, *args, **kwargs):
        return self.run_custom(
            soup=self.get_bs4(url=self.url, *args, **kwargs)
        )

    @abstractmethod
    def run_custom(self, soup):
        raise NotImplementedError()


class ArtistScraper(Base):

    @classmethod
    def build_url_path(cls, name):
        name = name.lower()
        return "{}/{}.html".format(
                name[0],
                name.replace(" ", "")
            )

    def __init__(self, url_or_name):
        super(ArtistScraper, self).__init__(url_or_name=url_or_name)

    def run_custom(self, soup):
        artist_name = soup.body.find("input", {"name": "artist"}).get("value")
        artist = Artist(name=artist_name)
        for child in soup.find("div", {"id": "listAlbum"}).children:
            if child.name == "div" and 'album' in child.get('class'):
                contents = child.contents
                group_type = contents[0].split(":")[0]
                name = contents[1].text.replace('"', '') if len(contents) > 1 else None
                year = contents[2].strip().strip("()") if len(contents) > 2 else None

                current_album = Album(
                        name=name,
                        year=year,
                        category=group_type
                )

                artist.albums.append(current_album)
                #print("{}: {} ({})".format(
                #    group_type, name, year
                #))
            elif child.name == 'a':
                current_album.songs.append(
                    SongScraper(parse.urljoin(self.url, child.get('href'))).run()
                )
                #print("Song: {} ({})".format(
                #    child.text,
                #    parse.urljoin(self.url, child.get('href'))
                #))

        return artist

    def exception_404_error(self, msg=None):
        return ArtistNotFound(msg)


class SongScraper(Base):

    def run_custom(self, soup):
        lyrics = None
        interesting_body = soup.body.find("div", {"class": "main-page"}).find("div", {"class": "row"}).\
            find(lambda tag: tag.name == "div" and "text-center" in tag['class'] and "noprint" not in tag['class'])
        name = interesting_body.findChild("b", recursive=False).text.replace('"', '')
        #for tag in soup.findAll("div"):
        #    if tag.name == "div" and not len(tag.attrs.keys()):
        #            lyrics=tag.text.strip()
        #
        #lyrics = interesting_body.findChild(
        #   lambda tag: tag.name=="div" and tag.get('class') == None,
        #   recursive=False
        #   ).text
        lyrics = soup.body.find(lambda tag: tag.name=="div" and not tag.get('class')).text
        #artist_name = soup.find("div", {"class" : "lyricsh"}).h2.b.text.replace(" Lyrics","")

        try:
            javascript = soup.body.find("script", recursive=False).text
            genre = re.search('\"([^\"]+)\"', javascript.replace("\r\n","")).groups()[0]
        except AttributeError as e:
            genre = None

        return Song(name=name, genre=genre, lyrics=clean_text(lyrics))

    def exception_404_error(self, msg=None):
        return SongNotFound(msg)

    @classmethod
    def build_url_path(cls, song_name, artist_name):
        artist_name = artist_name.lower()
        song_name = song_name.lower()
        return "{}/{}.html".format(
            artist_name.replace(" ", ""),
            song_name.replace(" ", "")
        )

    def __init__(self, url_or_name, artist_name=None):
        init_args = url_or_name if not artist_name else tuple((url_or_name, artist_name))
        super(SongScraper, self).__init__(url_or_name=init_args)

    def _clean_lyrics(self, lyrics):
        pass
