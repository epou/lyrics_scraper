class NotFound(Exception):
    pass


class ArtistNotFound(NotFound):
    pass


class SongNotFound(NotFound):
    pass


class LetterNotFound(NotFound):
    pass


class SearchScraperError(Exception):
    pass


class SearchEmptyResults(Exception):
    pass


class ArtistSearchEmptyResults(SearchEmptyResults):
    pass


class AlbumSearchEmptyResults(SearchEmptyResults):
    pass


class SongSearchEmptyResults(SearchEmptyResults):
    pass
