from fake_useragent import UserAgent
from random import randint
import requests as r
import time

max_delay_time_request = 15
min_delay_time_request = 7
batch_requests = 4


class Requester(object):
    """This class can perform batch requests with a random pause between them. Uses a fake useragent"""

    __counter = 0
    @classmethod
    def get(cls, url, instant=False):
        """Perform a GET request. If it's the last one of the batch, it'll perform a pause on the next request."""
        if cls.__counter >= batch_requests and not instant:
            # Wait a random time to avoid being banned
            rndint = randint(min_delay_time_request, max_delay_time_request)
            time.sleep(rndint)
            # Reset the counter
            cls.__counter = 0

        cls.__counter += 1
        # Set a random Useragent.
        headers = {'User-Agent': UserAgent().random}
        return r.get(url=url, headers=headers)
