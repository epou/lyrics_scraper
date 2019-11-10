from src.models import Song


def _build_dict(song: Song):
    return dict(
            artist=song.artist.name,
            album_name=song.album.name,
            album_year=song.album.year,
            album_category=song.album.category,
            song_name=song.name,
            song_genre=song.genre,
            song_lyrics=song.lyrics
    )


def __get_songs(result):
    return result.songs if not isinstance(result, Song) else [result]


def to_csv(output_file: str, songs: [Song]):
    import csv

    songs = __get_songs(result=songs)
    with open(output_file, 'a') as csv_file:
        writer = csv.DictWriter(
            f=csv_file,
            fieldnames=_build_dict(songs[0]).keys(),
            quoting=csv.QUOTE_MINIMAL
        )

        if csv_file.tell() == 0:
            writer.writeheader()

        for song in songs:
            writer.writerow(rowdict=_build_dict(song))
