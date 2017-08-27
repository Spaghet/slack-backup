from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import glob
import sys
import os
from slackviewer.main import main as slackviewer

domain = 'http://{team_name}.slack.com'
downloads = '' # ~/Downloads
slackviewer_path = '$(which slack-export-viewer)'
username = ''
password = ''

try:
    browser = webdriver.Chrome()
    browser.get('{}/services/export'.format(domain))
    browser.implicitly_wait(10)

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

    files = glob.glob('{}/*export*.zip'.format(downloads))
    newest = max(files, key=os.path.getctime)
    print(newest)

    sys.argv[0] = slackviewer_path
    sys.argv.append("-z")
    sys.argv.append(newest)
    slackviewer()

    browser.quit()
    print('done')
except Exception as e:
    print(e)
    browser.quit()
    pass
