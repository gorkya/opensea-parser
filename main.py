from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

url = 'https://opensea.io/explore-collections'

# driver – браузер, которому мы будем отдавать команды
s = Service("C:/Users/anast/PycharmProjects/opensea-parser/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=s)

# для сбора нужной информации и передачи в csv
info_dict = {'name': [],
             'best offer': [],
             'href': []}

# здесь наши запросы
try:
    driver.get(url=url)

    SCROLL_PAUSE_TIME = 1

    # получаем высоту прокрутки
    last_height = driver.execute_script("return document.body.scrollHeight")

    # цикл прокрутки
    while True:
        # прокручиваем вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # ждём загрузку страницы
        time.sleep(SCROLL_PAUSE_TIME)

        # получаем блок из всех NFT
        block = driver.find_element(By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div')

        # получаем названия всех NFT и добавляем в общий список
        info_dict['name'] += block.text.split('\n')

        # получаем ссылки на NFT и добавляем в общий список
        elements = block.find_elements(By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div > div > div > a')
        for element in elements:
            info_dict['href'].append(element.get_attribute('href'))

        # считаем новую высоту прокрутки и сравниваем со старой
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # открываем страницы NFT и вытаскиваем статистику
    for href in info_dict['href']:
        driver.get(href)
        element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div[5]/div/div[1]/div/div[3]/div/div[10]/a/div/span[1]/div')
        info_dict['best offer'].append(element.text)

# здесь будем выводить ошибки, если будут
except Exception as ex:
    print(ex)

# здесь код закрытия драйвера, который должен выполняться всегда, иначе будет куча болтающихся процессов в системе
finally:
    driver.close()
    driver.quit()

# записываем данные в csv файл
df = pd.DataFrame(info_dict)
df.to_csv('NFT.csv')
