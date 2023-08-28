import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time


@pytest.fixture(scope="function")
def browser():
    # Фикстура для инициализации и завершения работы веб-драйвера.
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def click_load_more_button(browser):
    # Нажимает на кнопку "загрузить ещё", если она присутствует на странице.
    try:
        while True:
            load_more_button = WebDriverWait(browser, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > div.css-f429t4 > "
                                  "button")))
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                load_more_button.click()
                time.sleep(5)
            else:
                break
    except TimeoutException:
        pass


def process_links(browser, visited_urls, urls_to_visit, start_domain):
    # Обрабатывает ссылки на странице, добавляя их в список для посещения.
    links = browser.find_elements(By.TAG_NAME, "a")
    for link in links:
        href = link.get_attribute("href")
        if href and urlparse(href).netloc == start_domain and href not in visited_urls and href not in urls_to_visit:
            urls_to_visit.append(href)


def test_canonical_link_and_images_alt(browser):
    # Тест для проверки канонических ссылок и тега alt изображений на страницах сайта.
    start_url = "https://trendtonext.com/"
    start_domain = urlparse(start_url).netloc
    visited_urls = set()
    urls_to_visit = [start_url]
    missing_canonical_links = []
    missing_alt_tags = []
    errors = []

    while urls_to_visit:
        current_url = urls_to_visit.pop()
        visited_urls.add(current_url)

        try:
            browser.get(current_url)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "footer")))

            process_links(browser, visited_urls, urls_to_visit, start_domain)

            canonical_links = browser.find_elements(By.CSS_SELECTOR, "link[rel='canonical']")
            if not canonical_links or canonical_links[0].get_attribute('href') is None:
                missing_canonical_links.append(current_url)

            click_load_more_button(browser)

            images = browser.find_elements(By.TAG_NAME, "img")
            for image in images:
                if image.get_attribute("alt") is None:
                    missing_alt_tags.append("Изображение без атрибута alt найдено на " + current_url)

        except Exception as e:
            errors.append("Ошибка на странице " + current_url + ": " + str(e))

    print("Canonical link и атрибут alt изображений проверены на {} страницах.".format(len(visited_urls)))
    print("Страницы без canonical link:", missing_canonical_links)
    print("Изображения без атрибута alt:", missing_alt_tags)
    if errors:
        print("Обнаружены следующие ошибки:")
        for error in errors:
            print(error)
