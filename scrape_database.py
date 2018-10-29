from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import requests
import csv

with open('base_case_100.csv') as csvfile:
	reader = csv.reader(csvfile)
	next(reader)
	next(reader)
	for row in reader:
		site = "https://oneweb.yolo.courts.ca.gov/OneWebCaseInquiry/#/CaseNumberSearch"

		time.sleep(2)

		driver = webdriver.Chrome("/Users/petermoung/Documents/yolo_hack/chromedriver")

		driver.implicitly_wait(5)
		driver.get(site)

		time.sleep(3)

		driver.find_element_by_css_selector('#memberModal > div > div > div.modal-footer > div > a.btn.btn-lg.btn-info').click()
		driver.implicitly_wait(5)
		driver.find_element_by_css_selector('#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(1) > div > select'
		                                  ).send_keys('Felony')
		driver.implicitly_wait(5)
		driver.find_element_by_css_selector('#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(1) > input').send_keys('2009')
		driver.implicitly_wait(5)
		driver.find_element_by_css_selector('#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(2) > input').send_keys('0148')
		driver.implicitly_wait(5)
		driver.find_element_by_css_selector('#content > div.ng-scope > div > div.panel-body > div.well > form > button').click()

		time.sleep(1)

		searchText = driver.find_element_by_class_name('ng-binding').text

		searchText = ' '.join(searchText.split())
		# match = soup.find('div', class_='ng-scope')

		time.sleep(1)

		test = row[2]

		new_test = ""

		flag = 0

		for c in test:
			if c == " " and flag == 0:
				flag = 1
				pass
			else:
				new_test += c

		test = new_test
		# print(new_test)








		result = re.search(r'%s' %test, searchText)

		if test.endswith('.'):
			test = test[:-3]

		if result:
			print(test + "confirmed name")

		else:
			print(test + "not confirmed name")




		# temp = row[2]

	

		# print(temp)




		time.sleep(3)

		driver.quit()



