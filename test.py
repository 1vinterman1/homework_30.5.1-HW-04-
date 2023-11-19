"""Практическое Задание 30.5.1 (HW-04)"""
import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC

chromedriver_autoinstaller.install()

@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()
   # Переходим на страницу авторизации
   driver.get('http://petfriends.skillfactory.ru/login')

   driver.maximize_window()
   yield driver

   driver.quit()


def test_show_my_pets(driver):
   wdw(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('qiki@mail.ru')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('1234')
   # Неявные ожидания
   driver.implicitly_wait(5)
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Нажимаем на кнопку "Мои питомцы"
   driver.find_element(By.CLASS_NAME, 'nav-item').click()
   # Проверяем, что мы оказались в разделе "Мои питомцы"
   assert driver.find_element(By.TAG_NAME, 'h2').text != " Qiki "
   # Явное ожидание
   wdw(driver, 5).until(EC.presence_of_element_located((By.ID, "all_my_pets")))


   images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')


   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0

