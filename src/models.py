class Artist(object):

    albums = []

    def __init__(self, name):
        self.name = name


class Album(object):

    songs = []

    def __init__(self, name, year, category):
        self.name = name
        self.year = year
        self.category = category


class Song(object):
    def __init__(self, name, genre, lyrics):
        self.name = name
        self.genre = genre
        self.lyrics = lyrics
