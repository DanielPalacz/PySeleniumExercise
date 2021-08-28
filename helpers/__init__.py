
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

import pytest


def get_timestamp():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H%M%S")
    return year + month + day + "_" + time


def output_directory(name):
    """Function:
    -- creates dedicated directory for the test results
    -- returns absolute path for the created directory"""
    dedicated_subdir = "Results//" + name
    try:
        os.mkdir(dedicated_subdir)
    except FileExistsError:
        dedicated_subdir += "_bis"
        os.mkdir(dedicated_subdir)

    return os.getcwd() + "//" + dedicated_subdir


class EbookWwwParser:

    SUPPORTED_CONTENT_TYPES = ["text/html"]

    def __init__(self, knowledgecenter_url, ebook_name, headers: dict = None):
        headers = headers if headers is not None else {}
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.ebook_name = ebook_name
        self.knowledgecenter_url = knowledgecenter_url
        self.all_ebook_links = None
        creation_msg = "EbookWwwParser object for url: " + self.knowledgecenter_url  + "was initiated."
        self.logger = logging.getLogger()
        self.logger.debug(creation_msg)

    def get_all_ebook_links(self):
        url = self.knowledgecenter_url
        self.logger.info("Get requests`s response object for url: %s", url)
        response = self.__fetch(url)

        if response and response.ok:
            content_type = response.headers.get("content-type", "")

            if any([1 if elem in content_type else 0 for elem in self.SUPPORTED_CONTENT_TYPES]):
                self.all_ebook_links = self.__extract(response.url, response.text)
            else:
                err_msg = "The url: '%s' has content type: %s which is not supported", url, content_type
                self.logger.info(err_msg)
                pytest.exit(err_msg)

        else:
            err_msg = "The given url could not be downloaded due to http code: %s", response.status_code
            self.logger.info(err_msg)
            pytest.exit(err_msg)

    def __fetch(self, url):
        self.logger.info(f"Fetching the given url: {url}")
        try:
            return self.session.get(url, allow_redirects=True)
        except requests.RequestException as e:
            return None

    def __extract(self, baseurl, text):
        soup = BeautifulSoup(text, "html.parser")
        links = soup.find_all("div", "ebook__img--container")
        hrefs = [link.find("a").get("href") for link in links]
        results = [urljoin(baseurl, link) for link in hrefs]
        self.logger.debug("Extracting links from the given url: %s", baseurl)
        return results


def if_ebook_is_placed_on_the_website(ebook_name, website_link):
    pass


if __name__ == "__main__":
    print(output_directory(get_timestamp()))
