from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from pathlib import Path

url = 'https://opensea.io/explore-collections'

driver = webdriver.Chrome()

driver.implicitly_wait(10)

# to collect the necessary information about NFT
info_dict = {}


# the function checks if there is an element with statistics on the page
def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        raise NoSuchElementException('error occurred')


try:
    driver.get(url=url)

    top_of_the_page = 0
    # scroll cycle
    while True:
        # scroll down
        bottom_of_the_page = driver.execute_script('return window.innerHeight + window.scrollY;')
        driver.execute_script(f'window.scrollTo(0,{bottom_of_the_page});')
        time.sleep(2)

        # get a block of all NFT which managed to boot
        several_loaded_NFTs = driver.find_element(By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div')

        list_of_several_loaded_NFTs = several_loaded_NFTs.find_elements(
            By.CSS_SELECTOR, '#main > div > div:nth-child(3) > div > div > div > div > div > a'
        )
        for NFT in list_of_several_loaded_NFTs:
            NFT_name = NFT.text
            href = NFT.get_attribute('href')
            info_dict.setdefault(NFT, [NFT_name, href])

        # compare the new scroll height with the old one
        if bottom_of_the_page == top_of_the_page:
            break
        top_of_the_page = bottom_of_the_page

    # open NFT pages, check statistics existence, add to the dict
    xpath = '//*[@id="main"]/div/div/div[5]/div/div[1]/div/div[3]/div/div[10]/a/div/span[1]/div'
    for NFT in info_dict:
        href = info_dict[NFT][1]
        driver.get(href)
        try:
            check_exists_by_xpath(xpath)
            statistics = driver.find_element(By.XPATH, xpath)
            info_dict[NFT].append(statistics.text)
        except NoSuchElementException:
            continue

except Exception as ex:
    print(ex)

finally:
    driver.close()
    driver.quit()

# write data to csv file
df = pd.DataFrame.from_dict(info_dict, orient='index')
df.columns = ["NFT name", "href", "best offer"]
absolute_path_to_the_current_directory = Path.cwd()
Path(absolute_path_to_the_current_directory, 'result').mkdir()
NFT_csv_path = Path(absolute_path_to_the_current_directory, 'result', 'NFT.csv')
df.to_csv(NFT_csv_path)
