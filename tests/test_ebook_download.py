"""Test scenario:
1. Open the following website: https://www.salesmanago.com/
2. Click 'Resources' tab.
3. Click 'Ebooks' tab.
4. Searching for the needed Ebook.
5. Going into Ebook specific page. Filling details needed for Ebook download.
6. Clicking Download button.
7. Clicking Download HERE button.
8. Verifying if the specific ebook was downloaded.
"""

from helpers import EbookWwwParser
from pages.MainPage import MainPage
from pages.KnowledgecenterPage import KnowledgeCenterPage
from pages.EbookPage import EbookPage
import pytest


@pytest.mark.parametrize("ebook_name",
                         [
                            "The Ultimate marketer's guide to Customer Data Platforms",
                            "Data Ethics & Customer Preference Management"
                         ])
def test_download_ebook(driver, helpers, ebook_name, name_and_surname, email, company, company_url, phone):
    """Test1: test_download_ebook."""

    log = helpers.get("logger")
    output_directory_path = helpers.get("output_directory_path")
    main_page = MainPage(driver, log)
    log.info("Starting executing: 'test_download_ebook' with: '" + ebook_name + "' parameter.")
    log.info("")
    log.info("Opening website: https://www.salesmanago.com/")
    main_page.driver.get("https://www.salesmanago.com/")
    main_page.click_resources_tab()
    main_page.click_ebooks_tab()

    log.info("Getting SALESmanago`s Knowledge center page url.")
    knowledge_center_page_url = main_page.driver.current_url

    log.info("Getting the ebook related url.")
    ebook_parser = EbookWwwParser(knowledge_center_page_url, ebook_name, log)
    ebook_parser.find_ebook_url()

    log.info("Clicking of the specific Ebook area.")

    knowledge_center_page = KnowledgeCenterPage(driver, log)
    knowledge_center_page.set_searched_ebook_xpath(ebook_parser.ebook_link)
    initial_window = knowledge_center_page.driver.current_window_handle
    knowledge_center_page.click_on_the_ebook_area()
    for window in knowledge_center_page.driver.window_handles:
        if window != initial_window:
            knowledge_center_page.driver.switch_to.window(window)
    log.info("Switching into newly opened Window (with details about teh Ebook).")

    log.info("Filling details needed for Ebook download.")
    ebook_page = EbookPage(driver, log)
    ebook_page.fill_name(name_and_surname)
    ebook_page.fill_email(email)
    ebook_page.fill_company(company)
    ebook_page.fill_company_url(company_url)
    ebook_page.fill_phone(phone)

    assert ebook_page.download(output_directory_path), "Ebook could not be downloaded"


if __name__ == "__main__":
    pass
