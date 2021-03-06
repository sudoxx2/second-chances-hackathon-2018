from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import requests
import csv

new_row_list = []

with open('mjData.csv') as csvfile:
    reader = csv.reader(csvfile)

    # skip first two rows. need to refactor
    next(reader)
    next(reader)

    for row in reader:

        num = 0

        site = "https://oneweb.yolo.courts.ca.gov/OneWebCaseInquiry/#/CaseNumberSearch"

        time.sleep(2)


        driver = webdriver.Chrome(
            "/Users/petermoung/Documents/yolo_hack/chromedriver")

        row3 = row[3]

        year = "20" + row3[:2]

        case_id = row3[4:]

        # print(year + " " + case_id)

        # get site and perform selenium actions
        driver.implicitly_wait(5)
        driver.get(site)
        time.sleep(3)
        driver.find_element_by_css_selector(
            '#memberModal > div > div > div.modal-footer > div > a.btn.btn-lg.btn-info').click()
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector('#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(1) > div > select'
                                            ).send_keys('Felony')
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector(
            '#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(1) > input').send_keys(year)
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector(
            '#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(2) > input').send_keys(case_id)
        driver.implicitly_wait(5)
        driver.find_element_by_css_selector(
            '#content > div.ng-scope > div > div.panel-body > div.well > form > button').click()
        time.sleep(1)

        # grab desired info to compare against data source
        searchText = driver.find_element_by_class_name('ng-binding').text
        searchText = ' '.join(searchText.split())

        time.sleep(1)

        # format data source to match against database
        row2 = row[2]

        if "JR" in row2:
            row2 = row2.replace(" JR, ", ", ")
        if "II" in row2:
            row2 = row2.replace(" II, ", ", ")
        if "III" in row2:
            row2 = row2.replace(" III, ", ", ")

        test = row2

        new_test = ""

        if test.endswith('.'):
            test = test[:-3]

        flag = 0

        for c in test:
            if c == " " and flag == 0:
                flag = 1
                pass
            else:
                new_test += c

        test = new_test



        result = re.search(r'%s' % test, searchText)

        # logic to perform csv action
        if result:
            print(test + " - confirmed name")
            num = 1
            new_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], num]
            new_row_list.append(new_row)
            print(new_row)
        else:
            driver.refresh()

            time.sleep(2)

            driver.get(site)
            time.sleep(3)
            driver.find_element_by_css_selector(
                '#memberModal > div > div > div.modal-footer > div > a.btn.btn-lg.btn-info').click()
            driver.implicitly_wait(5)
            driver.find_element_by_css_selector('#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(1) > div > select'
                                                ).send_keys('Misdemeanor')
            driver.implicitly_wait(5)
            driver.find_element_by_css_selector(
                '#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(1) > input').send_keys(year)
            driver.implicitly_wait(5)
            driver.find_element_by_css_selector(
                '#content > div.ng-scope > div > div.panel-body > div.well > form > div:nth-child(2) > input').send_keys(case_id)
            driver.implicitly_wait(5)
            driver.find_element_by_css_selector(
                '#content > div.ng-scope > div > div.panel-body > div.well > form > button').click()
            time.sleep(1)

            # grab desired info to compare against data source
            searchText = driver.find_element_by_class_name('ng-binding').text
            searchText = ' '.join(searchText.split())

            result = re.search(r'%s' % test, searchText)

            time.sleep(1)

            if result:
                print(test + " - confirmed name")
                num = 1
                new_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], num]
                new_row_list.append(new_row)
                print(new_row)
            else:
                print(test + " - not confirmed name")
                new_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], num]
                new_row_list.append(new_row)
                print(new_row)

        time.sleep(3)

        driver.quit()

with open('new_tester.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['Marijuana Cases - Data'])

    writer.writerows(new_row_list)

    csvfile.close()

