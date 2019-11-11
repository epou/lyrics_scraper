from src.scraper.search import ArtistSearcherScraper, AlbumSearcherScraper, SongSearcherScraper
from src.scraper.plain import LetterScraper

AVAILABLE_SEARCHERS = ("artist", "album", "song", "letter")


def get_searcher(name):
    if name == "artist":
        searcher = get_scraper_by_artist
    elif name == "album":
        searcher = get_scraper_by_album
    elif name == "song":
        searcher = get_scraper_by_song
    elif name == "letter":
        searcher = get_scraper_by_letter
    else:
        raise ValueError("Search by {} not available".format(name))

    return searcher


def __get_right_scraper(name, scraper, exact_search):

    if exact_search:
        result = scraper.RESULT_PAGE_SCRAPER()
        result = result(name)
    else:
        result = scraper(name).run()

    return result


def get_scraper_by_artist(name, exact_search=False):
    return __get_right_scraper(
        name=name,
        scraper=ArtistSearcherScraper,
        exact_search=exact_search
    )


def get_scraper_by_album(name, exact_search=False):
    return __get_right_scraper(
        name=name,
        scraper=AlbumSearcherScraper,
        exact_search=exact_search
    )


def get_scraper_by_song(name, exact_search=False):
    return __get_right_scraper(
        name=name,
        scraper=SongSearcherScraper,
        exact_search=exact_search
    )


def get_scraper_by_letter(letter):
    if not isinstance(letter, str):
        raise AttributeError("Letter must be a string")
    if len(letter) > 1:
        raise ValueError("Letter must be a single character.")
    return __get_right_scraper(
        name=letter,
        scraper=LetterScraper,
        exact_search=False
    )
