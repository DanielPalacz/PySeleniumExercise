
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    dedicated_subdir = "Results" + '/' + name
    try:
        os.mkdir(dedicated_subdir)
    except FileExistsError:
        dedicated_subdir += "_bis"
        os.mkdir(dedicated_subdir)

    return os.getcwd() + '/' + dedicated_subdir


class EbookWwwParser:

    SUPPORTED_CONTENT_TYPES = ["text/html"]

    def __init__(self, knowledgecenter_url, ebook_name, logger, headers: dict = None):
        headers = headers if headers is not None else {}
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.ebook_name = ebook_name
        self.ebook_link = None
        self.knowledgecenter_url = knowledgecenter_url
        self.all_ebook_links = None
        creation_msg = "EbookWwwParser object for url: " + self.knowledgecenter_url + "was initiated."
        self.logger = logger
        self.logger.debug(creation_msg)

    def __get_all_ebook_links(self):
        url = self.knowledgecenter_url
        self.logger.info(f"Get requests`s response object for url: {url}")
        response = self.__fetch(url)

        if response and response.ok:
            content_type = response.headers.get("content-type", "")

            if any([1 if elem in content_type else 0 for elem in self.SUPPORTED_CONTENT_TYPES]):
                self.all_ebook_links = self.__extract_ebook_links(response.url, response.text)
            else:
                err_msg = f"The url: '{url}' has content type: {content_type} which is not supported"
                self.logger.info(err_msg)
                pytest.exit(err_msg)

        else:
            err_msg = f"The given url could not be downloaded due to http code: {response.status_code}"
            self.logger.info(err_msg)
            pytest.exit(err_msg)

    def __fetch(self, url):
        self.logger.info(f" ** Fetching the given url: {url}")
        try:
            return self.session.get(url, allow_redirects=True)
        except requests.RequestException as e:
            return None

    def __extract_ebook_links(self, baseurl, text):
        self.logger.info("Extracting links for the all ebooks.")
        soup = BeautifulSoup(text, "html.parser")
        links = soup.find_all("div", "ebook__img--container")
        hrefs = [link.find("a").get("href") for link in links]
        results = [urljoin(baseurl, link) for link in hrefs]

        return results

    def find_ebook_url(self):
        self.logger.info("Finding the url link for the specific ebook.")
        self.__get_all_ebook_links()

        for potential_ebook_link in self.all_ebook_links:
            self.logger.info(f" ** Get requests`s response object for url: {potential_ebook_link}")
            response = self.__fetch(potential_ebook_link)
            self.logger.info(f" ** Checking if {potential_ebook_link} is related to searched: {self.ebook_name}")
            specific_ebook_soup = BeautifulSoup(response.text, "html.parser")
            links = specific_ebook_soup.find_all("h1", "ebook__title")
            if len(links) == 1 and links[0].text.strip() == self.ebook_name:
                self.logger.info(f" ** Searched ebook: {self.ebook_name} was found in: {potential_ebook_link}")
                self.ebook_link = potential_ebook_link
                break
        else:
            err_msg = "The ebook could not be found in list of all the ebook links (SALESmanago`s Knowledge center)"
            self.logger.info(err_msg)
            pytest.exit(err_msg)


if __name__ == "__main__":
    pass
