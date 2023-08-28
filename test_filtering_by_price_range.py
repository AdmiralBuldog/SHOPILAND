import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_price_filter(driver):
    # Открытие главной страницы
    driver.get("https://shopiland.ru/")

    # Ввод слова "велосипед" в строку поиска
    search_box = driver.find_element(By.CSS_SELECTOR,
                                     "#root > div > div.css-qxvndb > div > form > div > "
                                     "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.css"
                                     "-yp53iz > div > input")
    search_box.send_keys("велосипед")
    search_box.submit()

    # Задержка для загрузки результатов поиска
    time.sleep(15)

    # Ввод минимальной и максимальной цены
    min_price_input = driver.find_element(By.CSS_SELECTOR, "#min_price")
    min_price_input.send_keys("7000")
    time.sleep(5)  # задержка перед вводом максимальной цены
    max_price_input = driver.find_element(By.CSS_SELECTOR, "#max_price")
    max_price_input.send_keys("125000")

    # Задержка для применения фильтрации
    time.sleep(20)

    # Нажимаем на кнопку "загрузить ещё", пока она доступна
    while True:
        try:
            load_more_button = driver.find_element(By.CSS_SELECTOR, "#root > div > div > div.css-snude6 > "
                                                                    "div.MuiBox-root.css-woe6mf > div.css-f429t4 > "
                                                                    "button")
            load_more_button.click()
            time.sleep(5)  # Задержка для загрузки дополнительных товаров
        except NoSuchElementException:
            break  # Выходим из цикла, если кнопка "загрузить ещё" больше не найдена

    # Получение всех товаров на странице
    products = driver.find_elements(By.CSS_SELECTOR,
                                    "#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > "
                                    "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-isbt42 > div")

    # Сбор и сравнение цен
    min_price = float('inf')
    max_price = 0
    for product in products:
        price_element = product.find_element(By.CSS_SELECTOR, "div.MuiBox-root.css-bcvfj4 > span.css-bwtgpb")
        price_text = price_element.text.replace('\xa0', '').replace(' ', '').replace(',', '.').replace('₽', '').strip()
        price = float(price_text)
        min_price = min(min_price, price)
        max_price = max(max_price, price)

        if price < 7000 or price > 125000:
            description = product.find_element(By.CSS_SELECTOR, "div.MuiBox-root.css-0 > div > p").text
            print(
                f"Товар с описанием '{description}' имеет цену {price}, которая не соответствует диапазону 7000-125000")
            assert False

    print(f"Минимальная цена: {min_price}, Максимальная цена: {max_price}")
    print("Все цены соответствуют указанному диапазону")
