import pytest

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class KnowledgeCenterPage:
    """Page Object class for SALESmanago`s Knowledge center page:
    'https://www.salesmanago.com/info/knowledgecenter.htm"""

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.exp_wait = WebDriverWait(self.driver, 10, 0.5, NoSuchElementException)
        self.searched_ebook_xpath = None

    def set_searched_ebook_xpath(self, link):
        self.searched_ebook_xpath = "//a[contains(@href, '" + link + "')]"

    def click_on_the_ebook_area(self):
        """Clicking on the specific ebook."""

        ebooks_webelements = self.driver.find_elements_by_xpath(self.searched_ebook_xpath)
        if len(ebooks_webelements) == 1:
            ebooks_webelements[0].click()
        else:
            err_msg = "The issue with finding the unique Ebook webelement. Exiting."
            self.logger.info(err_msg)
            pytest.exit(err_msg)
