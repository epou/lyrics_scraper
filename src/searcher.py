from src.scraper.search import ArtistSearcherScraper, AlbumSearcherScraper, SongSearcherScraper
from src.scraper.plain import LetterScraper


def __get_right_scraper(name, search_type, exact_search):
    if search_type == "artist":
        scraper = ArtistSearcherScraper
    elif search_type == "album":
        scraper = AlbumSearcherScraper
    elif search_type == "song":
        scraper = SongSearcherScraper
    elif search_type == "letter":
        scraper = LetterScraper
    else:
        raise ValueError("Search by {} not available".format(search_type))

    if exact_search:
        result = scraper.RESULT_PAGE_SCRAPER()
        result = result(name)
    else:
        result = scraper(name).run()

    return result


def get_scraper_by_artist(name, exact_search=False):
    return __get_right_scraper(
        name=name,
        search_type="artist",
        exact_search=exact_search
    )


def get_scraper_by_album(name, exact_search=False):
    return __get_right_scraper(
        name=name,
        search_type="album",
        exact_search=exact_search
    )


def get_scraper_by_song(name, exact_search=False):
    return __get_right_scraper(
        name=name,
        search_type="song",
        exact_search=exact_search
    )


def get_scraper_by_letter(letter):
    if not isinstance(letter, str):
        raise AttributeError("Letter must be a string")
    if len(letter) > 1:
        raise ValueError("Letter must be a single character.")
    return __get_right_scraper(
        name=letter,
        search_type="letter",
        exact_search=False
    )
