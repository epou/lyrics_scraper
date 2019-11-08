from urllib import parse

from .scraper import ArtistScraper


class Base(object):
    PAGE_URL = "https://search.azlyrics.com/search.php?"


class ArtistSearcher(Base):

    QUERY_FILTER = 'artists'
    SCRAPER = ArtistScraper

    @classmethod
    def build_url(cls, name):
        return cls.PAGE_URL + cls.build_query(name=name)

    @classmethod
    def build_query(cls, name):
        return parse.urlencode(
            dict(
                q=parse.quote_plus(name),
                w=cls.QUERY_FILTER
            )
        )

    @classmethod
    def search_by_name(cls, name, lucky=True):
        if lucky:
            return ArtistScraper(url_or_name=name).run()
