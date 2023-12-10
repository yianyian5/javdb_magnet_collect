# define searching function
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def javdb_specific_page_magnet_collect(url = 'https://javdb523.com/lists/Gk1Gq?f=cnsub',page = 2):
    driver = webdriver.Chrome()
    driver.get(url)  
    driver.implicitly_wait(5)
    confirm_button = driver.find_element(By.XPATH, "//a[@class='button is-success is-large']")
    confirm_button.click()

    results = []
    for page in range(page):  # number_of_pages = 2 or 3
        time.sleep(5)  # waiting for the page to load
        items = driver.find_elements(By.CSS_SELECTOR, ".item")
        for item in items:
            link_element = item.find_element(By.CSS_SELECTOR, "a.box")
            url = link_element.get_attribute('href')
            
            title_element = item.find_element(By.CSS_SELECTOR, "div.video-title strong")
            title = title_element.text
        
            score_element = item.find_element(By.CSS_SELECTOR, "div.score span.value")
            score = score_element.text.strip()
            
            results.append((title, url, score))
        try:
            next_page_link = driver.find_element(By.XPATH,"//a[contains(@class, 'pagination-next')]")
            driver.get(next_page_link.get_attribute('href'))
        except:
            pass
        time.sleep(5)
        
    results = pd.DataFrame(results, columns=['title', 'url', 'score'])
    for index in range(results.shape[0]):
        row = results.iloc[index]
        driver.get(row['url'])
        time.sleep(2)
        try:
            confirm_button = driver.find_element(By.XPATH, "//a[@class='button is-success is-large']")
            confirm_button.click()
        except:
            pass
        items = driver.find_elements(By.CSS_SELECTOR, ".item.columns.is-desktop.odd, .item.columns.is-desktop")
        magnet_link = None
        for item in items:
            if item.find_elements(By.XPATH,".//span[contains(text(), '高清')]") and item.find_elements(By.XPATH,".//span[contains(text(), '字幕')]"):
                magnet_link = item.find_element(By.XPATH,".//a[contains(@href, 'magnet')]").get_attribute('href')
                break  
        results.loc[index, 'magnet_link'] = magnet_link
    return results
results = javdb_specific_page_magnet_collect(url = 'https://javdb523.com/lists/Gk1Gq?f=cnsub',page = 4)
results.to_excel('javdb_top2023.xlsx', index=False)