from functools import reduce


class Song(object):
    """Song model.

    It contains all the relevant information about a song.
    """

    def __init__(self, name, genre, lyrics):
        """Constructor."""
        self.name = name
        self.genre = genre
        self.lyrics = lyrics
        self.album = None

    @property
    def artist(self):
        """Returns the artist of the song."""
        return self.album.artist if self.album else None

    def __str__(self):
        return "<Song: {}>".format(self.name)

    def __repr__(self):
        return self.__str__()


class Album(object):
    """Album model.

    It contains all the relevant information about an album.
    """

    def __init__(self, name, year, category):
        """Constructor"""
        self.name = name
        self.year = year
        self.category = category
        self.__songs = []
        self.artist = None

    @property
    def songs(self):
        """Returns all the songs of the album."""
        return self.__songs

    def add_song(self, song: Song):
        """Adds a song into the album."""
        self.__songs.append(song)
        song.album = self

    def __str__(self):
        return "<{}: {} ({})>".format(self.category.title(), self.name, self.year)

    def __repr__(self):
        return self.__str__()


class Artist(object):
    """Artist model.

    It contains all the relevant information about an artist.
    """

    def __init__(self, name):
        """Constructor"""
        self.name = name
        self.__albums = []

    @property
    def albums(self):
        """Returns all the albums of the artist."""
        return self.__albums

    @property
    def songs(self):
        """Returns all the songs of the artist."""
        return reduce(lambda x, y: x+y, [album.songs for album in self.albums])

    def add_album(self, album: Album):
        """Add and album to the artist."""
        self.__albums.append(album)
        album.artist = self

    def __str__(self):
        return "<Artist: {}>".format(self.name)

    def __repr__(self):
        return self.__str__()
