import re
from urllib import parse

# Custom imports
from src.models import Album, Artist, Song
from src.scraper.base import BaseScraper
from src.scraper.exceptions import ArtistNotFound, SongNotFound, LetterNotFound
from src.utils import clean_text


class ArtistScraper(BaseScraper):

    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        return ArtistNotFound

    @classmethod
    def build_url_path(cls, name):
        name = name.lower()
        return "{}/{}.html".format(
                name[0],
                name.replace(" ", "")
            )

    def run_custom(self, soup, album_id=None, *args, **kwargs):
        artist_name = soup.body.find("input", {"name": "artist"}).get("value")
        artist = Artist(name=artist_name)

        album_filter = {"class": "album"}
        if album_id:
            album_filter["id"] = album_id

        for album in soup.body.find("div", {"id": "listAlbum"}).find_all("div", album_filter):
            #contents = album.contents
            name, year, category = AlbumScraper.get_album_parameters_from_content(contents=album.contents)
            current_album = Album(
                name=name,
                year=year,
                category=category
            )
            artist.add_album(current_album)
            for sibling in album.next_siblings:
                if sibling.name == "a":
                    current_album.add_song(
                        SongScraper(
                            parse.urljoin(
                                self.url,
                                sibling.get('href')
                            )
                        ).run(search_album=False)
                    )
                elif sibling.name == "div":
                    # next album
                    break

        return artist


class SongScraper(BaseScraper):

    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        return SongNotFound

    @classmethod
    def build_url_path(cls, song_name, artist_name):
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
        interesting_body = soup.body.find("div", {"class": "main-page"}).find("div", {"class": "row"}).\
            find(lambda tag: tag.name == "div" and "text-center" in tag['class'] and "noprint" not in tag['class'])
        name = interesting_body.findChild("b", recursive=False).text.replace('"', '')
        #for tag in soup.findAll("div"):
        #    if tag.name == "div" and not len(tag.attrs.keys()):
        #            lyrics=tag.text.strip()
        #
        #lyrics = interesting_body.findChild(
        #   lambda tag: tag.name=="div" and tag.get('class') == None,
        #   recursive=False
        #   ).text
        lyrics = soup.body.find(lambda tag: tag.name=="div" and not tag.get('class')).text
        #artist_name = soup.find("div", {"class" : "lyricsh"}).h2.b.text.replace(" Lyrics","")

        try:
            javascript = soup.body.find("script", recursive=False).text
            genre = re.search('\"([^\"]+)\"', javascript.replace("\r\n","")).groups()[0]
        except AttributeError as e:
            genre = None

        result = Song(name=name, genre=genre, lyrics=clean_text(lyrics))
        if search_album:
            # Get artist
            artist_name = soup.body.find("div", {"class": "lyricsh"}).h2.b.text.replace(" Lyrics", "")
            artist = Artist(artist_name)
            # Get album
            temp_soup = soup.body.find("div", {"class": "songlist-panel"})

            if temp_soup:
                for element in temp_soup.find_all(lambda tag: tag.name == "a" or tag.name == "br"):
                    _ = element.extract()

                name, year, category = AlbumScraper.get_album_parameters_from_content(
                    contents=[x for x in temp_soup.contents if x != '\n']
                )

                album = Album(name=name, year=year, category=category)
                album.artist = artist
                result.album = album

        return result


class AlbumScraper(ArtistScraper):

    @classmethod
    def get_album_parameters_from_content(cls, contents):
        if isinstance(contents, list):
            #contents_cleaned = [x.replace("\n", "").replace("\r", "").strip() for x in contents]

            name = contents[1].text.replace('"', '').strip() if len(contents) > 1 else None
            year = contents[2].strip().strip("()").strip() if len(contents) > 2 else None
            category = contents[0].replace("\n", "").replace("\r", "").strip().split(":")[0]
            return name, year, category
        return None, None, None

    def __init__(self, url):
        url_parsed = parse.urlparse(url)
        self.album_id = url_parsed.fragment
        
        super(AlbumScraper, self).__init__(url)

    def run_custom(self, soup, *args, **kwargs):
        result = super().run_custom(soup, self.album_id).albums
        return result[0] if result else None


class LetterScraper(BaseScraper):
    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        return LetterNotFound

    @classmethod
    def build_url_path(cls, letter, *args, **kwargs):
        return "{}.html".format(letter)

    def run_custom(self, soup, *args, **kwargs):
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
