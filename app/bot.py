
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def check_article():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-gpu')

  driver = webdriver.Chrome(chrome_options=chrome_options)
  driver.get('http://127.0.0.1/login')
  driver.find_element_by_id('user_id').send_keys('admin')
  driver.find_element_by_id('user_pw').send_keys('noflaghere')
  driver.find_element_by_id('login').submit()
  #print driver.page_source
  driver.get('http://127.0.0.1/qna')
  driver.find_element_by_xpath(
    '//table[@id="qna"]/tbody/tr[not(@class="pinned-row")]/td[@class="title"]/a[1]'
  ).click()
  #print driver.page_source
  time.sleep(3)
  driver.close()
