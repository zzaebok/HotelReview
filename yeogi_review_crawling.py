import pickle
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument("disable-gpu")
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
provinces = ['서울','대전','대구','부산','울산', '광주','인천']
review_list = []

for province in provinces:
    url = 'https://www.goodchoice.kr/product/result?keyword='
    url += province
    driver.get(url)
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > b > footer > div > ul > li:nth-child(1) > a')))
    html = driver.page_source
    soup = bs(html, 'html.parser')
    lists = soup.find_all('li', {'class': 'list_4 adcno1'})
    for list in lists:
        try:
            hotel_url = list.find('a')['href']
            driver.get(hotel_url)
            html = driver.page_source
            soup = bs(html, 'html.parser')
            review_button = driver.find_element_by_xpath('//*[@id="content"]/div[2]/button[3]')
            review_button.click()
            time.sleep(.5)
            num_review = driver.find_element_by_xpath('//*[@id="review_cnt"]/em')
            num_review = int(num_review.text.replace(',',''))
            iteration = int(num_review/50)
        except Exception as e:
            print(e)
            continue

        for iter in range(iteration):
            for num in range(5):
                try:
                    if iter==0:    #start page
                        next = driver.find_element_by_xpath('//*[@id="pagination"]/div/button['+str(num+1)+']')
                        next.click()
                        time.sleep(.5)
                    else:
                        next = driver.find_element_by_xpath('//*[@id="pagination"]/div/button['+str(num+2)+']')
                        next.click()
                        time.sleep(.4)
                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.wrap.show > footer > div > div > a.icon-ic_facebook')))
                    html = driver.page_source
                    soup = bs(html, 'html.parser')
                    scores = soup.find_all('div', {'class': 'num'})[1:]
                    sentences = [guest_review.find('div', {'class': 'txt'}) for guest_review in soup.find_all('div', {'class': 'guest'})[1:]]
                    for x in range(10):
                        review_list.append((sentences[x].text, scores[x].text))
                except Exception as e:
                    print(e)
                    continue
            try:
                if iter==0:
                    driver.find_element_by_xpath('//*[@id="pagination"]/div/button[6]').click()
                    time.sleep(.4)
                else:
                    driver.find_element_by_xpath('//*[@id="pagination"]/div/button[7]').click()
                    time.sleep(.5)
            except Exception as e:
                print(e)
                continue

with open('yeogi.pkl', 'wb') as f:
    pickle.dump(review_list, f)