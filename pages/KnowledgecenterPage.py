import pytest

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions


class KnowledgeCenterPage:
    """Page Object class for SALESmanago`s Knowledge center page:
    'https://www.salesmanago.com/info/knowledgecenter.htm"""

    def __init__(self, webdriver_el, logger):
        self.driver = webdriver_el
        self.logger = logger
        self.exp_wait = WebDriverWait(self.driver, 10, 0.5, NoSuchElementException)
        #
