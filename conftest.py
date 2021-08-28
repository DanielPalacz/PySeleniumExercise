import pytest
import logging
from helpers import get_timestamp
from helpers import output_directory


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException


@pytest.fixture()
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--lang=pl")
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    except WebDriverException:
        pass
    # self.driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture()
def helpers():
    """helpers fixture"""

    timestamp = get_timestamp()
    output_directory_path = output_directory(timestamp)

    logger = logging.getLogger(__file__)
    ch = logging.FileHandler(output_directory_path + "//log.txt")
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return {"logger": logger, "timestamp": timestamp}


if __name__ == "__main__":
    pass
