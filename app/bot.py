
# Copyright (C) 2019 Xvezda <https://xvezda.com/>

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-gpu')

driver = webdriver.Chrome('./driver/chromedriver', chrome_options=chrome_options)
driver.get('http://localhost:8080/login')
driver.find_element_by_name('user_id').send_keys('admin')
driver.find_element_by_name('user_pw').send_keys('noflaghere')
driver.find_element_by_id('login').submit()
print driver.page_source
driver.close()
