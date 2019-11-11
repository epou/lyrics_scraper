# Custom imports
from src.scraper.base import BaseSearchScraper
from src.scraper.plain import AlbumScraper, ArtistScraper, SongScraper
from src.scraper.exceptions import AlbumSearchEmptyResults, ArtistSearchEmptyResults, SongSearchEmptyResults


class ArtistSearcherScraper(BaseSearchScraper):
    """This class defines how an scraper (in search.azlyrics.com) must act given an artist name."""

    @classmethod
    def RESULT_PAGE_SCRAPER(cls):
        return ArtistScraper

    @classmethod
    def QUERY_LABEL(cls):
        return 'artists'

    @classmethod
    def EXCEPTION_EMPTY_RESULTS(cls):
        return ArtistSearchEmptyResults


class AlbumSearcherScraper(BaseSearchScraper):
    """This class defines how an scraper (in search.azlyrics.com) must act given an album name."""

    @classmethod
    def RESULT_PAGE_SCRAPER(cls):
        return AlbumScraper

    @classmethod
    def EXCEPTION_EMPTY_RESULTS(cls):
        return AlbumSearchEmptyResults

    @classmethod
    def QUERY_LABEL(cls):
        return 'albums'


class SongSearcherScraper(BaseSearchScraper):
    """This class defines how an scraper (in search.azlyrics.com) must act given a song name."""

    @classmethod
    def RESULT_PAGE_SCRAPER(cls):
        return SongScraper

    @classmethod
    def EXCEPTION_EMPTY_RESULTS(cls):
        return SongSearchEmptyResults

    @classmethod
    def QUERY_LABEL(cls):
        return 'songs'
