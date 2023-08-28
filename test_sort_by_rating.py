import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_sorted_by_rating():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие главной страницы сайта
    driver.get("https://shopiland.ru/")

    # Ввод ключевого слова "ноутбуки" в поле поиска
    search_field_selector = ("#root > div > div.css-qxvndb > div > form > div > "
                             "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.css-yp53iz > "
                             "div > input")
    search_field = driver.find_element(By.CSS_SELECTOR, search_field_selector)
    search_field.send_keys("ноутбуки")
    search_field.submit()
    time.sleep(20)  # Задержка для загрузки всех товаров

    # Клик по кнопке сортировки по рейтингу
    rating_button_selector = "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button[2]"
    rating_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, rating_button_selector)))
    rating_button.click()
    time.sleep(20)  # Задержка для применения сортировки

    # Получение рейтингов товаров
    ratings_selector = "//div[contains(@class, 'MuiBox-root') and contains(@aria-label, '.')]"
    ratings_elements = driver.find_elements(By.XPATH, ratings_selector)
    ratings = [float(rating_element.get_attribute('aria-label')) for rating_element in ratings_elements]

    # Проверка, что первый товар имеет рейтинг 5.00
    assert ratings[0] == 5.00, f"Первый товар имеет рейтинг {ratings[0]}"

    # Проверка, что все остальные товары имеют рейтинг 5.00 или меньше
    for rating in ratings[1:]:
        assert rating <= 5.00, f"Товар имеет рейтинг {rating}, который больше 5.00"

    # Закрытие драйвера
    driver.quit()
