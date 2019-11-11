from src.scraper.search import ArtistSearcherScraper, AlbumSearcherScraper, SongSearcherScraper
from src.scraper.plain import LetterScraper

AVAILABLE_SEARCHERS = ("artist", "album", "song", "letter")


def get_searcher(name):
    """Returns the right function given a name (search by the name)"""
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
    # Case the user is sure of the search.
    if exact_search:
        # Return the scraper pending to be run.
        result = scraper.RESULT_PAGE_SCRAPER()
        result = result(name)
    else:
        # Return the result of the scraper once run.
        result = scraper(name).run()

    return result


def get_scraper_by_artist(name, exact_search=False):
    """Returns all the available scraper given an artist name."""
    return __get_right_scraper(
        name=name,
        scraper=ArtistSearcherScraper,
        exact_search=exact_search
    )


def get_scraper_by_album(name, exact_search=False):
    """Returns all the available scraper given an album name."""
    return __get_right_scraper(
        name=name,
        scraper=AlbumSearcherScraper,
        exact_search=exact_search
    )


def get_scraper_by_song(name, exact_search=False):
    """Returns all the available scraper given a song name."""
    return __get_right_scraper(
        name=name,
        scraper=SongSearcherScraper,
        exact_search=exact_search
    )


def get_scraper_by_letter(letter):
    """Returns all the available scraper given a letter."""

    # Check the letter format. Raise error if needed.
    if not isinstance(letter, str):
        raise AttributeError("Letter must be a string")
    if len(letter) > 1:
        raise ValueError("Letter must be a single character.")

    return __get_right_scraper(
        name=letter,
        scraper=LetterScraper,
        exact_search=False
    )
