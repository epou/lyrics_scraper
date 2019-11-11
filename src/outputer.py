from src.models import Song


def _build_dict(song: Song):
    """Given a song return a dict with all the parameters."""
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
    """Returns an array of songs given a result."""
    return result.songs if not isinstance(result, Song) else [result]


def to_csv(output_file: str, songs: [Song]):
    """Generate a CSV with the the information of all the songs."""
    import csv

    # Get the songs list.
    songs = __get_songs(result=songs)

    # Append into the output_file.
    with open(output_file, 'a') as csv_file:
        # Build a writer from the dictionary.
        writer = csv.DictWriter(
            f=csv_file,
            fieldnames=_build_dict(songs[0]).keys(),
            quoting=csv.QUOTE_MINIMAL
        )

        if csv_file.tell() == 0:
            # Write headers if the file is empty.
            writer.writeheader()

        for song in songs:
            # Write the info of each song into a new row.
            writer.writerow(rowdict=_build_dict(song))
