#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import os

domain = 'http://{}.slack.com'.format(os.environ['SLACK_TEAM'])
downloads = os.environ['SLACK_BACKUP_DIR'] # ~/Downloads
username = os.environ['SLACK_USER']
password = os.environ['SLACK_PASS']

browser = webdriver.Chrome()

try:
    print('opening page')
    browser.get('{}/services/export'.format(domain))
    browser.implicitly_wait(10)

    print('logging in')
    username_elem = browser.find_element_by_id('email')
    password_elem = browser.find_element_by_id('password')
    submit_elem = browser.find_element_by_id('signin_btn')

    username_elem.send_keys(username)
    password_elem.send_keys(password + Keys.RETURN)

    print('logged in!')
    try:
        button = browser.find_element_by_tag_name('button')
        print(button)
        button.click()
    except:
        print('error in button')
        pass

    table = False
    while not table:
        try:
            print('??')
            table = browser.find_element_by_id('export_history')
        except Exception as e:
            print(e)
            browser.refresh()

    latest_link = table.find_elements_by_tag_name('td')[2].find_element_by_tag_name('a')
    latest_link.click()

    print('done')
except:
    browser.close()

browser.close()
