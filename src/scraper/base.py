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

max_delay_time_request = 20
min_delay_time_request = 0


class BaseScraper(ABC):
    ALLOWED_ITERABLE_INPUT = (list, tuple)
    ALLOWED_NON_ITERABLE_INPUT = (str)

    BASE_PAGE_URL = "https://www.azlyrics.com/"

    @classmethod
    def build_url(cls, *args, **kwargs):
        return parse.urljoin(
            base=cls.BASE_PAGE_URL,
            url=cls.build_url_path(*args, **kwargs)
        )

    @classmethod
    def _check_response(cls, response):
        try:
            response.raise_for_status()
        except HTTPError as e:
            if response.status_code == r.codes.not_found:
                raise cls.EXCEPTION_NOT_FOUND() from None
            else:
                raise

    @classmethod
    def _do_request(cls, url, instant=False, *args, **kwargs):
        return Requester.get(url=url, instant=instant)

    @classmethod
    def _get_bs4(cls, url, features='html.parser', *args, **kwargs):
        response = cls._do_request(url=url, *args, **kwargs)
        cls._check_response(response=response)
        soup = BeautifulSoup(
            markup=response.text,
            features=features
        )

        cls._clean_soup(soup=soup, *args, **kwargs)
        return soup

    @classmethod
    def _clean_soup(cls, soup, remove_tags=None, *args, **kwargs):
        _ = [x.extract() for x in soup(remove_tags)] if remove_tags else None
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
        url = None
        if isinstance(url_or_name, self.ALLOWED_ITERABLE_INPUT):
            url = self.build_url(*url_or_name)
        elif isinstance(url_or_name, self.ALLOWED_NON_ITERABLE_INPUT):
            url = url_or_name if is_url(url_or_name) else self.build_url(url_or_name)

        self.url = url

    def run(self, *args, **kwargs):
        return self.run_custom(
            soup=self._get_bs4(url=self.url, *args, **kwargs),
            *args,
            **kwargs
        )


class BaseSearchScraper(BaseScraper):

    BASE_PAGE_URL = "https://search.azlyrics.com/"

    @classmethod
    def EXCEPTION_NOT_FOUND(cls):
        raise SearchScraperError

    @classmethod
    def build_url_path(cls, name):
        return "search.php?" + parse.urlencode(
            dict(
                q=name,
                w=cls.QUERY_LABEL()
            )
        )

    @classmethod
    def result_is_empty(cls, soup, raise_if_empty=False):
        result = True if soup.body.find("div", {"class": "alert"}) else False
        if raise_if_empty and result:
            raise cls.EXCEPTION_EMPTY_RESULTS() from None
        return result

    def run_custom(self, soup, *args, **kwargs):
        plain_scraper = self.RESULT_PAGE_SCRAPER()
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
