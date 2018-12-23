import pickle
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument("disable-gpu")
driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)


url_first = 'https://www.tripadvisor.co.kr/Hotels-g297893-'
url_last = '-Ulsan-Hotels.html'
url_list = []
pos_list = []
neg_list = []
i = 0


for x in range(1,10):
    url = url_first+'oa'+str(x*30)+url_last
    try:
        driver.get(url)
    except:
        continue
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'taplc_main_pagination_bar_dusty_hotels_resp_0')))
    html = driver.page_source
    soup = bs(html, 'html.parser')
    cand = soup.find_all('a', {'class': 'review_count'})
    for can in cand:
        url = 'https://www.tripadvisor.co.kr/' + can['href']
        url_list.append(url)

    for url in url_list:
        try:

            driver.get(url)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "taplc_global_footer_0")))
            html = driver.page_source
            soup = bs(html, 'html.parser')
            time.sleep(1)
            very_good = driver.find_element_by_xpath('//*[@id="taplc_detail_filters_hr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[1]')
            very_good.click()
            time.sleep(1)
            more = driver.find_element_by_xpath('//span[contains(., "{}") and @class="taLnk ulBlueLinks"]'.format('더 보기'))
            time.sleep(1)
            more.click()
            time.sleep(3)
            #더보기는 잘 클릭되는데, 리뷰가 지멋대로 똑같이 처박힌다. 그리고 더보기 이후의 텍스트가 담기는게아님.
            reviews = driver.find_elements_by_css_selector('div.ui_column.is-9 > div.prw_rup.prw_reviews_text_summary_hsx > div > p')
            for review in reviews:
                pos_list.append(review.text)
            very_good = driver.find_element_by_xpath('//*[@id="taplc_detail_filters_hr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[1]')
            very_good.click()
            time.sleep(1)

            very_bad = driver.find_element_by_xpath('//*[@id="taplc_detail_filters_hr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[5]')
            very_bad.click()
            time.sleep(1)
            more = driver.find_element_by_xpath('//span[contains(., "{}") and @class="taLnk ulBlueLinks"]'.format('더 보기'))
            time.sleep(1)
            more.click()
            time.sleep(3)
            reviews = driver.find_elements_by_css_selector('div.ui_column.is-9 > div.prw_rup.prw_reviews_text_summary_hsx > div > p')
            for review in reviews:
                neg_list.append(review.text)
        except Exception as ea:
            print(ea)


driver.quit()

with open('pos_list_ulsan.pkl', 'wb') as f:
    pickle.dump(pos_list, f)

with open('neg_list_ulsan.pkl', 'wb') as f:
    pickle.dump(neg_list, f)