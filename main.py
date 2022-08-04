from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

url = 'https://opensea.io/explore-collections'

driver = webdriver.Chrome()

driver.implicitly_wait(10)

# to collect the necessary information and transfer to csv
info_dict = {'name': [],
             'best offer': [],
             'href': []}


# the function checks if there is an element with statistics on the page
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


try:
    driver.get(url=url)

    top_of_the_page = 0
    # scroll cycle
    while True:
        # scroll down
        bottom_of_the_page = driver.execute_script('return window.innerHeight + window.scrollY;')
        driver.execute_script(f'window.scrollTo(0,{bottom_of_the_page});')
        time.sleep(2)

        # get a block of all NFT
        block = driver.find_element(By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div')

        # get all NFT names, check for absence in the list and add to the list
        for name in block.text.split('\n'):
            if name not in info_dict['name']:
                info_dict['name'].append(name)

        # get NFT urls, check for absence in the list and add to the list
        elements = block.find_elements(
            By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div > div > div > a'
        )
        for element in elements:
            href = element.get_attribute('href')
            if href not in info_dict['href']:
                info_dict['href'].append(href)

        # compare the new scroll height with the old one
        if bottom_of_the_page == top_of_the_page:
            break
        top_of_the_page = bottom_of_the_page

    # open NFT pages, check statistics existence, add to the list
    for href in info_dict['href']:
        driver.get(href)
        if check_exists_by_xpath('//*[@id="main"]/div/div/div[5]/div/div[1]/div/div[3]/div/div[10]/a/div/span[1]/div'):
            element = driver.find_element(
                By.XPATH, '//*[@id="main"]/div/div/div[5]/div/div[1]/div/div[3]/div/div[10]/a/div/span[1]/div'
            )
            info_dict['best offer'].append(element.text)
        else:
            info_dict['best offer'].append(None)

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()

# write data to csv file
df = pd.DataFrame(info_dict)
df.to_csv('NFT.csv')
