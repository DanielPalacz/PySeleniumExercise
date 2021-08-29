import pytest
import logging
from helpers import get_timestamp
from helpers import output_directory


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException


@pytest.fixture()
def driver(helpers):

    log = helpers.get("logger")
    output_directory_path = helpers.get("output_directory_path")
    log.info("")
    log.info("")
    log.info("")
    log.info("")
    log.info("Configuring driver object.")

    chrome_options = Options()
    chrome_options.add_argument("--lang=pl")
    chrome_options.add_experimental_option('prefs', {
        "download.default_directory": output_directory_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    except WebDriverException:
        pass

    driver.maximize_window()
    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def helpers(pytestconfig):
    """helpers fixture"""

    timestamp = get_timestamp()
    output_directory_path = output_directory(timestamp)
    pytestconfig.option.output_directory_path = output_directory_path

    logger = logging.getLogger(__file__)
    ch = logging.FileHandler(output_directory_path + "//log.txt")
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return {"logger": logger, "output_directory_path": output_directory_path}


@pytest.fixture()
def name_and_surname():
    return "Jan Kowalski"


@pytest.fixture()
def email():
    return "jan.kowalski.benhauer+testrekrutacja@salesmanago.com"


@pytest.fixture()
def company():
    return "SALESmanago"


@pytest.fixture()
def company_url():
    return "https://www.salesmanago.com"


@pytest.fixture()
def phone():
    return "555666777"


@pytest.mark.trylast
def pytest_sessionfinish(session):
    try:
        import shutil
        import os
        shutil.copy(os.getcwd() + '/' + session.config.option.htmlpath, session.config.option.output_directory_path)
    except:
        print("Something happened during copying report to specific result location.")
    print()
    print()
    print("=========================================")
    print("Hi. I am 'pytest_sessionfinish' Pytest Hook. I want to tell you that: Python Selenium exercise ended.")
    print("=========================================")


if __name__ == "__main__":
    pass
