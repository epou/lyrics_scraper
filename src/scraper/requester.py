from fake_useragent import UserAgent
from random import randint
import requests as r
import time

max_delay_time_request = 15
min_delay_time_request = 5
batch_requests = 4


class Requester(object):
    __counter = 0
    @classmethod
    def get(cls, url, instant=False):

        if cls.__counter >= batch_requests and not instant:
            # Wait a random time to avoid being banned
            rndint = randint(min_delay_time_request, max_delay_time_request)
            time.sleep(rndint)

            cls.__counter = 0

        cls.__counter += 1
        # Set a random Useragent.
        headers = {'User-Agent': UserAgent().random}
        return r.get(url=url, headers=headers)
