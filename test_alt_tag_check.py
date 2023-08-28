import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_images_have_alt_attribute(driver):
    # Открытие страницы для проверки alt тэга
    driver.get("https://shopiland.ru/search?q=%D0%B2%D0%B5%D0%BE%D0%BB%D1%81%D0%B8%D0%BF%D0%B5%D0%B4")

    # Ожидание появления кнопки "загрузить ещё"
    while True:
        try:
            load_more_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > div.css-f429t4 > button")))
            if load_more_button.is_displayed() and load_more_button.is_enabled():
                load_more_button.click()
                # Ожидание, чтобы дать время для загрузки новых изображений
                time.sleep(5)
            else:
                break
        except TimeoutException:
            break

    # Получение всех изображений на странице
    images = driver.find_elements(By.TAG_NAME, "img")

    # Проверка, что у каждого изображения есть атрибут alt
    for image in images:
        assert image.get_attribute("alt") is not None, "Изображение без атрибута alt найдено"

    print(f"Все {len(images)} изображений на странице содержат атрибут alt.")
