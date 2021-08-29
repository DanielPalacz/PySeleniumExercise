
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions

import os


class EbookPage:
    """Page Object class for the specific Ebook - when was chosen from SALESmanago`s Knowledge center."""

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.exp_wait = WebDriverWait(self.driver, 10, 0.5, NoSuchElementException)
        self.ebook_exp_wait = WebDriverWait(self.driver, 10, 0.5)
        self.name_xpath = "//input[@type='text'][@name='name']"
        self.email_xpath = "//input[@type='email'][@name='email']"
        self.company_xpath = "//input[@type='text'][@name='company']"
        self.company_url_xpath = "//input[@type='text'][@name='url']"
        self.phone_xpath = "//input[@type='tel'][@name='phoneNumber']"
        self.download_button_xpath = "//form/div/div/button[@type='submit']"
        self.download_here_button_xpath = "//a[text()='HERE']"
        #
        self.logger.info("Was initiated the Page Object for the specific ebook.")

    def fill_name(self, name):
        self.driver.find_element_by_xpath(self.name_xpath).send_keys(name)

    def fill_email(self, email):
        self.driver.find_element_by_xpath(self.email_xpath).send_keys(email)

    def fill_company(self, company):
        self.driver.find_element_by_xpath(self.company_xpath).send_keys(company)

    def fill_company_url(self, company_url):
        self.driver.find_element_by_xpath(self.company_url_xpath).send_keys(company_url)

    def fill_phone(self, phone):
        self.driver.find_element_by_xpath(self.phone_xpath).send_keys(phone)

    def download(self, output_directory_path):
        self.logger.info("Downloading the specific ebook.")
        self.logger.info("Clicking 'Download' button.")
        self.driver.find_element_by_xpath(self.download_button_xpath).click()
        self.exp_wait.until(expected_conditions.element_to_be_clickable((By.XPATH, self.download_here_button_xpath)))
        tuple_with_file_names_before_starting_downloading = self.get_fileresults_list(output_directory_path)
        self.logger.info("Clicking 'Download Here' button.")
        self.driver.find_element_by_xpath(self.download_here_button_xpath).click()
        self.logger.info("Verifying if that given ebook was downloaed")
        return self.download_observer(output_directory_path, tuple_with_file_names_before_starting_downloading)

    def get_fileresults_list(self, output_directory_path):
        self.logger.info("Getting the tuple with list of files inside Result directory.")
        files = os.listdir(output_directory_path)
        return tuple(files)

    def download_observer(self, absolute_path, tuple_with_file_names_before_starting_downloading):
        import time
        t_0 = time.time()
        time.sleep(1)
        download_in_progress = True
        while download_in_progress:
            self.logger.info(" ** Download observer continues ")
            t_progress = int(time.time() - t_0)
            time.sleep(1)
            files_when_download_started = os.listdir(absolute_path)
            if len(files_when_download_started) > len(tuple_with_file_names_before_starting_downloading):
                self.logger.info(" ** Download observer found the ebook placed in Result directory.")
                return True
            if t_progress > 10:
                self.logger.info(" ** Download observer exceeded time set for monitoring. ")
                return False
            self.logger.info(" ** Download observer continues monitoring process.")


class EbookDownloadingHasBeenDone:
    """Custom Wait Condition for checking that given ebook has been successfully downloaded.
    """

    def __init__(self, absolute_path, tuple_with_file_names_before_starting_downloading):
        self.absolute_path = absolute_path
        self.tuple_with_file_names_before_starting_downloading = tuple_with_file_names_before_starting_downloading

    def __call__(self):
        files_when_download_started = os.listdir(self.absolute_path)
        if len(files_when_download_started) > len(self.tuple_with_file_names_before_starting_downloading):
            return True
        else:
            return False
