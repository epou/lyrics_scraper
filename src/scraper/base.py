from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests as r
from requests.exceptions import HTTPError
from urllib import parse

# Custom imports
from src.utils import is_url
from src.scraper.exceptions import SearchScraperError
from src.scraper.requester import Requester


class BaseScraper(ABC):
    """This class is an abstract class that define how an scraper (in azlyrics) must act."""
    ALLOWED_ITERABLE_INPUT = (list, tuple)
    ALLOWED_NON_ITERABLE_INPUT = (str)

    BASE_PAGE_URL = "https://www.azlyrics.com/"

    @classmethod
    def build_url(cls, *args, **kwargs):
        """Return the url"""
        return parse.urljoin(
            base=cls.BASE_PAGE_URL,
            url=cls.build_url_path(*args, **kwargs)
        )

    @classmethod
    def _check_response(cls, response):
        """Checks if the response is not 200 and raise a custom error."""
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == r.codes.not_found:
                raise cls.EXCEPTION_NOT_FOUND() from None
            else:
                raise

    @classmethod
    def _do_request(cls, url, instant=False, *args, **kwargs):
        """Perform a GET request."""
        return Requester.get(url=url, instant=instant)

    @classmethod
    def _get_bs4(cls, url, features='html.parser', *args, **kwargs):
        """Create and return a Beautiful soup object given an url"""
        # Perform the get requests
        response = cls._do_request(url=url, *args, **kwargs)
        # Check for error response
        cls._check_response(response=response)
        # Generate a BeautifulSoup object
        soup = BeautifulSoup(
            markup=response.content.decode(encoding=response.apparent_encoding, errors='ignore'),
            features=features
        )

        # Clean the beautiful soup object
        cls._clean_soup(soup=soup, *args, **kwargs)
        return soup

    @classmethod
    def _clean_soup(cls, soup, remove_tags=None, *args, **kwargs):
        """Given a BeautifulSoup object, remove the given tags and comments"""
        # Remove all the tags inside remove_tags parameter.
        _ = [x.extract() for x in soup(remove_tags)] if remove_tags else None
        # Remove all the comments.
        _ = [x.extract() for x in soup.find_all(text=lambda text: isinstance(text, Comment))]

    @classmethod
    @abstractmethod
    def EXCEPTION_NOT_FOUND(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def build_url_path(cls, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def run_custom(self, soup, *args, **kwargs):
        raise NotImplementedError

    def __init__(self, url_or_name):
        """Constructor"""
        # If it's already an url -> store it.
        # If it's not an url -> build the url using the build_url function defined above.
        url = None
        if isinstance(url_or_name, self.ALLOWED_ITERABLE_INPUT):
            url = self.build_url(*url_or_name)
        elif isinstance(url_or_name, self.ALLOWED_NON_ITERABLE_INPUT):
            url = url_or_name if is_url(url_or_name) else self.build_url(url_or_name)

        self.url = url

    def run(self, *args, **kwargs):
        """Run the scraper"""
        return self.run_custom(
            soup=self._get_bs4(url=self.url, *args, **kwargs),
            *args,
            **kwargs
        )


class BaseSearchScraper(BaseScraper):
    """This class is an abstract class that define how an scraper (in search.azlyrics.com) must act."""

    BASE_PAGE_URL = "https://search.azlyrics.com/"

    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        # Override
        raise SearchScraperError

    @classmethod
    def build_url_path(cls, name):
        """Build the correct url for the searcher given a name."""
        return "search.php?" + parse.urlencode(
            dict(
                q=name,
                w=cls.QUERY_LABEL()
            )
        )

    @classmethod
    def result_is_empty(cls, soup, raise_if_empty=False):
        """Check if the result of the search is empty or not"""
        # Check if a "div" tag with the class "alert" is found or not in the beautiful soup object.
        result = True if soup.body.find("div", {"class": "alert"}) else False

        # Raise if needed.
        if raise_if_empty and result:
            raise cls.EXCEPTION_EMPTY_RESULTS() from None
        return result

    def run_custom(self, soup, *args, **kwargs):
        """Return a list with all the scrapers result of the search. Scrapers are pending to run."""
        plain_scraper = self.RESULT_PAGE_SCRAPER()
        # Return a tuple (immutable) of all the href attributes results inside:
        #       * first "div" tag, which class is "panel"
        #       * all "a" tags without a class, to avoid the pagination "a" tags.
        # If the result is empty, return an empty list.
        return tuple(
            [
                plain_scraper(tag.get('href')) for tag in soup.body.find("div", {"class": "panel"}).find_all(
                    lambda tag: tag.name == "a" and not tag.get('class')
                )
            ]
        ) if not self.result_is_empty(soup, *args, **kwargs) else []

    @classmethod
    @abstractmethod
    def RESULT_PAGE_SCRAPER(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def EXCEPTION_EMPTY_RESULTS(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def QUERY_LABEL(cls):
        raise NotImplementedError
