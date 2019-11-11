import re
from urllib import parse

# Custom imports
from src.models import Album, Artist, Song
from src.scraper.base import BaseScraper
from src.scraper.exceptions import ArtistNotFound, SongNotFound, LetterNotFound
from src.utils import clean_text


class ArtistScraper(BaseScraper):
    """This class defines how an scraper (in azlyrics) must act given the artist url."""

    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        # Overrides
        return ArtistNotFound

    @classmethod
    def build_url_path(cls, name):
        """Build the correct url for the artist given a name."""
        name = name.lower()
        return "{}/{}.html".format(
                name[0],
                name.replace(" ", "")
            )

    def run_custom(self, soup, album_id=None, *args, **kwargs):
        """Returns an artist object with the result of scraping all its albums and songs."""

        # Get the artist name, and generate a new Artist object.
        artist_name = soup.body.find("input", {"name": "artist"}).get("value")
        artist = Artist(name=artist_name)

        # In case album_id is set, we need to get only that album. We filter the result.
        album_filter = {"class": "album"}
        if album_id:
            # Adding another key in the dict to filter the following results.
            album_filter["id"] = album_id

        # For every album in the filtered soup (with the album_id if needed).
        for album in soup.body.find("div", {"id": "listAlbum"}).find_all("div", album_filter):

            # Get the album parameters and crate a new Album object.
            name, year, category = AlbumScraper.get_album_parameters_from_content(contents=album.contents)
            current_album = Album(
                name=name,
                year=year,
                category=category
            )
            # Add the album into the artist.
            artist.add_album(current_album)

            # Lets get all the songs.
            for sibling in album.next_siblings:
                if sibling.name == "a":
                    # In case it's an "a" tag, we know it's a song.
                    # Let's add into the album the new song (result of the SongScraper after running it)
                    # We build the SongScraper with the result of joining the current URL and the path given in the
                    # current 'href' attribute of the "a" tag.
                    current_album.add_song(
                        SongScraper(
                            parse.urljoin(
                                self.url,
                                sibling.get('href')
                            )
                        ).run(search_album=False)
                    )
                elif sibling.name == "div":
                    # We are on the next album. Break the iteration
                    break
        # Return the artist
        return artist


class SongScraper(BaseScraper):
    """This class defines how an scraper (in azlyrics) must act given the song url."""

    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        return SongNotFound

    @classmethod
    def build_url_path(cls, song_name, artist_name):
        """Build the correct url for the song given a name."""
        artist_name = artist_name.lower()
        song_name = song_name.lower()
        return "{}/{}.html".format(
            artist_name.replace(" ", ""),
            song_name.replace(" ", "")
        )

    def __init__(self, url_or_name, artist_name=None):
        init_args = url_or_name if not artist_name else (url_or_name, artist_name)
        super(SongScraper, self).__init__(url_or_name=init_args)

    def run_custom(self, soup, search_album=True, *args, **kwargs):
        """Returns a song object with the result of scraping all its parameters and the lyrics."""

        # The interesting part of the HTML code is inside:
        #       * The first "div" which class is "main-page".
        #       * The first "div" which class is "row"
        #       * The first "div" which class contains "text-center" but no "noprint".
        interesting_body = soup.body.find("div", {"class": "main-page"}).find("div", {"class": "row"}).\
            find(lambda tag: tag.name == "div" and "text-center" in tag['class'] and "noprint" not in tag['class'])

        # Get the song name without double quotes.
        name = interesting_body.findChild("b", recursive=False).text.replace('"', '')

        # Get all the lyrics.
        lyrics = soup.body.find(lambda tag: tag.name == "div" and not tag.get('class')).text

        try:
            # Let's take the genre. It's found inside a JS object.
            javascript = soup.body.find("script", recursive=False).text
            genre = re.search('\"([^\"]+)\"', javascript.replace("\r\n", "")).groups()[0]
        except AttributeError as e:
            genre = None

        # Build a Song object with all the parameters. We clean the lyrics before.
        result = Song(name=name, genre=genre, lyrics=clean_text(lyrics))

        # Case we need to search the album too
        if search_album:
            # Get artist name and build an Artist object.
            artist_name = soup.body.find("div", {"class": "lyricsh"}).h2.b.text.replace(" Lyrics", "")
            artist = Artist(artist_name)
            # Get album name
            temp_soup = soup.body.find("div", {"class": "songlist-panel"})

            # In case the album name has been found
            if temp_soup:
                # Remove all the tags that are "a" or "br" to clean the HTML part we need.
                for element in temp_soup.find_all(lambda tag: tag.name == "a" or tag.name == "br"):
                    _ = element.extract()

                # Get the album parameters.
                name, year, category = AlbumScraper.get_album_parameters_from_content(
                    contents=[x for x in temp_soup.contents if x != '\n']
                )

                # Create a new Album object
                album = Album(name=name, year=year, category=category)
                # Assign the artist to the album
                album.artist = artist
                # Assign the album to the result song.
                result.album = album

        return result


class AlbumScraper(ArtistScraper):
    """This class defines how an scraper (in azlyrics) must act given the album url."""

    @classmethod
    def get_album_parameters_from_content(cls, contents):
        if isinstance(contents, list):
            name = contents[1].text.replace('"', '').strip() if len(contents) > 1 else None
            year = contents[2].strip().strip("()").strip() if len(contents) > 2 else None
            category = contents[0].replace("\n", "").replace("\r", "").strip().split(":")[0]
            return name, year, category
        return None, None, None

    def __init__(self, url):
        # The album id is passed in the URL as a fragment (after the "#" character). Let's parse it.
        url_parsed = parse.urlparse(url)
        self.album_id = url_parsed.fragment
        
        super(AlbumScraper, self).__init__(url)

    def run_custom(self, soup, *args, **kwargs):
        """Returns an album object with the result of scraping all its songs."""
        # In this particular case, we have to use the same method as the parent (ArtistScraper) due to it's the same
        # plain webpage, with the diference we only need a particular album (given the album_id) instead of all
        # of them.
        result = super().run_custom(soup, self.album_id).albums
        return result[0] if result else None


class LetterScraper(BaseScraper):
    """This class defines how an scraper (in azlyrics) must act given the single letter url."""

    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        return LetterNotFound

    @classmethod
    def build_url_path(cls, letter, *args, **kwargs):
        """Build the correct url for the letter given a character."""
        return "{}.html".format(letter)

    def run_custom(self, soup, *args, **kwargs):
        """Returns a list of ArtistScraper ready to be run"""
        # Build a list with all ArtistScraper result of the 'href' attribute of all the "a" tags inside the
        # "div" tag which class is "artist-col". Avoid the external link by filtering those "a" tags which
        # have a class, the good ones are those which doesn't have any class.
        return [
            ArtistScraper(
                parse.urljoin(
                    self.BASE_PAGE_URL,
                    x.get('href')
                )
            ) for x in soup.body.find("div", {"class": "artist-col"}).find_all(
                lambda tag: tag.name == "a" and not tag.get('class')
            )
        ]
