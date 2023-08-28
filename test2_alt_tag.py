import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def click_load_more_button(driver):
    # Нажимает кнопку "загрузить ещё", если она присутствует на странице.
    try:
        while True:
            load_more_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > div.css-f429t4 > button")))
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                load_more_button.click()
                time.sleep(5)
            else:
                break
    except TimeoutException:
        pass


def check_images_alt_attribute(driver, current_url):
    # Проверяет наличие атрибута alt у всех изображений на текущей странице.
    images = driver.find_elements(By.TAG_NAME, "img")
    for image in images:
        assert image.get_attribute("alt") is not None, f"Изображение без атрибута alt найдено на {current_url}"


def get_internal_links(driver, start_url, visited_urls):
    # Возвращает все внутренние ссылки на текущей странице, которые еще не были посещены.
    links = driver.find_elements(By.TAG_NAME, "a")
    hrefs = [link.get_attribute("href") for link in links]
    return [href for href in hrefs if href and urlparse(href).netloc == urlparse(start_url).netloc and href not in visited_urls]


def test_images_have_alt_attribute(driver):
    # Тест для проверки наличия атрибута alt у всех изображений на сайте.
    start_url = "https://shopiland.ru/"
    visited_urls = set()
    urls_to_visit = [start_url]

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        visited_urls.add(current_url)

        driver.get(current_url)

        click_load_more_button(driver)
        check_images_alt_attribute(driver, current_url)
        urls_to_visit.extend(get_internal_links(driver, start_url, visited_urls))

    print(f"Все изображения на {len(visited_urls)} страницах содержат атрибут alt.")
