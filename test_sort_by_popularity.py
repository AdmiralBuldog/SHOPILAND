import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_sorted_by_popularity():
    # Инициализация драйвера
    driver = webdriver.Chrome()

    # Открытие главной страницы сайта
    driver.get("https://shopiland.ru/")

    # Ожидание до 10 секунд
    wait = WebDriverWait(driver, 10)

    # Ввод ключевого слова "ноутбуки" в поле поиска
    search_field_selector = (
        "#root > div > div.css-qxvndb > div > form > div > "
        "div.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.css-yp53iz > div "
        "> input"
    )
    search_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, search_field_selector)))
    search_field.send_keys("ноутбуки")
    search_field.send_keys(Keys.RETURN)

    # Клик по кнопке сортировки по популярности
    popularity_button_selector = "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button[3]/div"
    wait.until(EC.element_to_be_clickable((By.XPATH, popularity_button_selector))).click()

    # Получение популярности самого популярного товара
    most_popular_selector = (
        "#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > "
        "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-isbt42 > div:nth-child(1) > div "
        "> div > a > div.MuiBox-root.css-0 > div > div.MuiBox-root.css-bp8b62 > span"
    )
    most_popular_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, most_popular_selector)))
    most_popular_text = most_popular_element.text.replace(' ', '').replace('₽', '').replace(',', '.')
    most_popular_number = re.sub(r'[^\d.]+', '', most_popular_text)
    most_popular = float(most_popular_number)

    # Получение популярности самого непопулярного товара
    least_popular_selector = (
        "#root > div > div > div.css-snude6 > div.MuiBox-root.css-woe6mf > "
        "div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.css-isbt42 > div:nth-child(60) > "
        "div > div > a > div.MuiBox-root.css-0 > div > div.MuiBox-root.css-bp8b62 > span"
    )
    least_popular_text = driver.find_element(By.CSS_SELECTOR, least_popular_selector).text.replace(' ', '').replace('₽',
                                                                                                                    '').replace(
        ',', '.')
    least_popular_number = re.sub(r'[^\d.]+', '', least_popular_text)
    least_popular = float(least_popular_number)

    assert most_popular >= least_popular, (
        f"Популярность самого популярного товара {most_popular} меньше популярности "
        f"самого непопулярного товара {least_popular}"
    )

    # Закрытие драйвера
    driver.quit()

    print("Тест сортировки по популярности успешно пройден")
