from src.scraper.search import ArtistSearcherScraper, AlbumSearcherScraper, SongSearcherScraper


def __get_right_scraper(name, search_type, exact_search):
    if search_type == "artist":
        scraper = ArtistSearcherScraper
    elif search_type == "album":
        scraper = AlbumSearcherScraper
    elif search_type == "song":
        scraper = SongSearcherScraper
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
