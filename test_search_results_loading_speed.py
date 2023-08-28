import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Фикстура для инициализации и завершения работы с драйвером
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


# Параметризация теста для проверки с разными запросами поиска
@pytest.mark.parametrize("query", ["ноутбук", "велосипед", "samsung s22 ultra"])
def test_search_loading_time(driver, query):
    # Открытие страницы
    driver.get("https://shopiland.ru/")

    # Ожидание загрузки строки поиска
    wait = WebDriverWait(driver, 30)
    search_field_selector = ("#root > div > div.css-qxvndb > div > form > div > "
                             "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.css-yp53iz > "
                             "div > input")
    search_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, search_field_selector)))

    # Ввод ключевого слова из параметра
    search_field.send_keys(query)
    search_field.send_keys(Keys.RETURN)

    # Ожидание открытия страницы с результатами поиска
    results_selector = ("#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > "
                        "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-isbt42")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, results_selector)))

    # Начало отсчета времени
    start_time = time.time()

    # Ожидание исчезновения строки загрузки
    loading_selector = ("#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > div.MuiBox-root.css-1blh15x "
                        "> div")
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, loading_selector)))

    # Расчет времени загрузки
    load_time = time.time() - start_time

    # Проверка, что время загрузки не превышает 20 секунд
    assert load_time <= 20, f"Тест не пройден для запроса '{query}', ответ загружается за {load_time} секунд"
