# Custom imports
from src.scraper.base import BaseSearchScraper
from src.scraper.plain import AlbumScraper, ArtistScraper, SongScraper
from src.scraper.exceptions import AlbumSearchEmptyResults, ArtistSearchEmptyResults, SongSearchEmptyResults


class ArtistSearcherScraper(BaseSearchScraper):

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
    @classmethod
    def RESULT_PAGE_SCRAPER(cls):
        return SongScraper

    @classmethod
    def EXCEPTION_EMPTY_RESULTS(cls):
        return SongSearchEmptyResults

    @classmethod
    def QUERY_LABEL(cls):
        return 'songs'
