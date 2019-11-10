from functools import reduce


class Song(object):

    def __init__(self, name, genre, lyrics):
        self.name = name
        self.genre = genre
        self.lyrics = lyrics
        self.album = None

    @property
    def artist(self):
        return self.album.artist if self.album else None

    def __str__(self):
        return "<Song: {}>".format(self.name)

    def __repr__(self):
        return self.__str__()


class Album(object):

    def __init__(self, name, year, category):
        self.name = name
        self.year = year
        self.category = category
        self.__songs = []
        self.artist = None

    @property
    def songs(self):
        return self.__songs

    def add_song(self, song: Song):
        self.__songs.append(song)
        song.album = self

    def __str__(self):
        return "<{}: {} ({})>".format(self.category.title(), self.name, self.year)

    def __repr__(self):
        return self.__str__()


class Artist(object):

    def __init__(self, name):
        self.name = name
        self.__albums = []

    @property
    def albums(self):
        return self.__albums

    @property
    def songs(self):
        return reduce(lambda x, y: x+y, [album.songs for album in self.albums])

    def add_album(self, album: Album):
        self.__albums.append(album)
        album.artist = self

    def __str__(self):
        return "<Artist: {}>".format(self.name)

    def __repr__(self):
        return self.__str__()
