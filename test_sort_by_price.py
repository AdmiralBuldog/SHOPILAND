import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Фикстура для инициализации и завершения работы с драйвером
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


# Параметризация тестов для проверки с разными запросами поиска
@pytest.mark.parametrize("query", ["ноутбук", "телефон", "велосипед"])
def test_sort_by_price(driver, query):
    print(f"Тестирование сортировки для запроса: {query}")

    # Открытие главной страницы сайта
    driver.get("https://shopiland.ru/")

    # Ввод ключевого слова в поле поиска
    search_field_selector = ("#root > div > div.css-qxvndb > div > form > div > "
                             "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.css-yp53iz > "
                             "div > input")
    search_field = driver.find_element(By.CSS_SELECTOR, search_field_selector)
    search_field.send_keys(query)
    search_field.send_keys(Keys.RETURN)
    time.sleep(10)  # Дать время для загрузки страницы

    # Селектор кнопки сортировки по цене
    sort_button_selector = "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button[1]"
    sort_button = driver.find_element(By.XPATH, sort_button_selector)
    sort_button.click()
    time.sleep(10)  # Дать время для применения сортировки

    # Проверка сортировки от минимальной к максимальной
    check_sorting(driver, reverse=False)

    # Нажатие на кнопку сортировки по цене еще раз для сортировки в обратном порядке
    sort_button.click()
    time.sleep(10)  # Дать время для применения сортировки

    # Проверка сортировки от максимальной к минимальной
    check_sorting(driver, reverse=True)


def check_sorting(driver, reverse=False):
    # Получение всех новых цен
    prices_selector = ("#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > "
                       "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-isbt42 > div > div > "
                       "div > a > div.MuiBox-root.css-0 > div > div.MuiBox-root.css-bcvfj4 > span.css-bwtgpb")
    prices_elements = driver.find_elements(By.CSS_SELECTOR, prices_selector)
    prices = [float(price.text.replace(' ', '').replace('₽', '').replace(',', '.')) for price in prices_elements]

    # Проверка сортировки с учетом возможных дубликатов
    for i in range(len(prices) - 1):
        if reverse:
            assert prices[i] >= prices[i + 1], "Цены не отсортированы в убывающем порядке"
        else:
            assert prices[i] <= prices[i + 1], "Цены не отсортированы в возрастающем порядке"

    print(f"Тест сортировки по цене в {'убывающем' if reverse else 'возрастающем'} порядке успешно пройден")


# Запуск всех тестов
if __name__ == "__main__":
    pytest.main(["-v"])
