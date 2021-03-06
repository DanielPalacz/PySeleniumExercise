import pytest

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions


class MainPage:
    """Page Object class for SALESmanago`s main page: 'https://www.salesmanago.com/"""

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.exp_wait = WebDriverWait(self.driver, 10, 0.5, NoSuchElementException)
        self.resources_xpath = "//a[contains(@class, 'custom-lowbar__link')][text()='resources']"
        self.ebooks_xpath = "//a[contains(@class, 'dropdown__link')][text()='Ebooks']"
        self.logger.info("Was initiated the Page Object for: 'https://www.salesmanago.com")

    def click_resources_tab(self):
        """Clicking 'Resources' tab."""
        self.logger.info("Clicking 'Resources' tab.")
        self.exp_wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.resources_xpath)))
        resources_webelements = self.driver.find_elements_by_xpath(self.resources_xpath)
        if len(resources_webelements) == 1:
            resources_webelements[0].click()
        else:
            err_msg = "The issue with finding the unique 'Resources' tab webelement. Exiting."
            self.logger.info(err_msg)
            pytest.exit(err_msg)

    def click_ebooks_tab(self):
        """Clicking 'Ebooks' tab."""
        self.logger.info("Clicking 'Ebooks' tab.")
        self.exp_wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.ebooks_xpath)))
        ebooks_webelements = self.driver.find_elements_by_xpath(self.ebooks_xpath)
        if len(ebooks_webelements) == 1:
            ebooks_webelements[0].click()
        else:
            err_msg = "The issue with finding the unique 'Ebooks' tab webelement. Exiting."
            self.logger.info(err_msg)
            pytest.exit(err_msg)
