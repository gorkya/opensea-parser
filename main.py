from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

url = 'https://opensea.io/explore-collections'

# driver – браузер, которому мы будем отдавать команды
s = Service("C:/Users/anast/PycharmProjects/opensea-parser/chromedriver/chromedriver.exe")
driver = webdriver.Chrome(service=s)

# driver будет ждать максимум 10 сек перед тем, как появится какой-то элемент
driver.implicitly_wait(10)

# для сбора нужной информации и передачи в csv
info_dict = {'name': [],
             'best offer': [],
             'href': []}


# функция проверяет, есть ли вообще элемент со статистикой на странице
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# здесь наши запросы
try:
    driver.get(url=url)

    h_prev = 0
    # цикл прокрутки
    while True:
        # прокручиваем вниз
        h = driver.execute_script('return window.innerHeight + window.scrollY;')
        driver.execute_script(f'window.scrollTo(0,{h});')
        time.sleep(2)

        # получаем блок из всех NFT
        block = driver.find_element(By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div')

        # получаем названия всех NFT и добавляем в общий список, проверяя на отсутствие в списке
        for name in block.text.split('\n'):
            if name not in info_dict['name']:
                info_dict['name'].append(name)

        # получаем ссылки на NFT и добавляем в общий список, проверяя на отсутствие в списке
        elements = block.find_elements(
            By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div > div > div > a'
        )
        for element in elements:
            href = element.get_attribute('href')
            if href not in info_dict['href']:
                info_dict['href'].append(href)

        # новую высоту прокрутки сравниваем со старой
        if h == h_prev:
            break
        h_prev = h

    # открываем страницы NFT и вытаскиваем статистику, проверяя её наличие на странице
    for href in info_dict['href']:
        driver.get(href)
        if check_exists_by_xpath('//*[@id="main"]/div/div/div[5]/div/div[1]/div/div[3]/div/div[10]/a/div/span[1]/div'):
            element = driver.find_element(
                By.XPATH, '//*[@id="main"]/div/div/div[5]/div/div[1]/div/div[3]/div/div[10]/a/div/span[1]/div'
            )
            info_dict['best offer'].append(element.text)
        else:
            info_dict['best offer'].append(None)

# здесь будем выводить ошибки, если будут
except Exception as ex:
    print(ex)

# здесь код закрытия драйвера, который должен выполняться всегда, иначе будет куча болтающихся процессов в системе
finally:
    driver.close()      # закрывает вкладку
    driver.quit()       # закрывает браузер

# записываем данные в csv файл
df = pd.DataFrame(info_dict)
df.to_csv('NFT.csv')
