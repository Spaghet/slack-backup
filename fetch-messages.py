#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import boto3

import sys
import os
import glob

# Get the config options for your slack user
domain = 'http://{}.slack.com'.format(os.environ['SLACK_TEAM'])
downloads = os.environ['SLACK_BACKUP_DIR'] # ~/Downloads
username = os.environ['SLACK_USER']
password = os.environ['SLACK_PASS']

# Get config for S3
bucket_name = os.environ['BUCKET_NAME']

# Set chromium options to run in headless mode
options = Options()
options.add_argument('--headless')

# Set the download directory and other settings
pref = {'download.default_directory': downloads,
                     'download.prompt_for_download': False,
                     'download.directory_upgrade': True,
                     'safebrowsing.enabled': False,
                     'safebrowsing.disable_download_protection': True}
options.add_experimental_option('prefs', pref)

browser = webdriver.Chrome(chrome_options=options)

browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

# Download files when in headless mode
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': downloads}}
command_result = browser.execute("send_command", params)

try:
    print('opening page')
    browser.get('{}/services/export'.format(domain))
    browser.implicitly_wait(10)

    # command_result = browser.execute('send_command', params)

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
except Exception as e:
    print(e)
    browser.close()

# Wait until the download is completed
files = []
while len(files) == 0:
    files = glob.glob('{}/*export*.zip'.format(downloads))

newest = max(files, key=os.path.getctime)

# Upload the file to S3
s3 = boto3.resource('s3')
with open(newest, 'rb') as file:
    s3.Bucket(bucket_name).put_object(Key=newest, Body=file)

browser.close()
