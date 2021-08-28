"""Test scenario:
1. Open the following website: https://www.salesmanago.com/
2. Click 'Resources' tab
3. Click 'Ebooks' tab
4.
5.
"""

from helpers import EbookWwwParser
from pages.MainPage import MainPage
from pages.KnowledgecenterPage import KnowledgeCenterPage
import pytest


from msedge.selenium_tools import Edge, EdgeOptions
from msedge.selenium_tools.remote_connection import EdgeRemoteConnection
from selenium import webdriver


def test_download_ebook(driver, helpers):
    """Test1: test_download_ebook."""

    log = helpers.get("logger")
    timestamp = helpers.get("timestamp")
    main_page = MainPage(driver, log)

    log.info("Opening website: https://www.salesmanago.com/")
    main_page.driver.get("https://www.salesmanago.com/")
    main_page.click_resources_tab()
    main_page.click_ebooks_tab()
    # knowledge_center_page = KnowledgeCenterPage(driver, log)

    log.info("Getting SALESmanago`s Knowledge center page url.")
    knowledge_center_page_url = main_page.driver.current_url
    ebook_name = "ebook_name"
    ebook_parser = EbookWwwParser(knowledge_center_page_url, ebook_name)
    ebook_parser.get_all_ebook_links()
    print()
    print()
    print(ebook_parser.all_ebook_links)
    input()


if __name__ == "__main__":
    pass
