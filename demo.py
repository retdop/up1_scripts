import os
os.chdir('/home/gabriel/xberkeley/up1/up1_scripts')
import up1.data_scraping as ds
import math
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
#%%

def open_bob(driver):
    driver.get('https://retdop.github.io')


def write_something_normally(text, element, delay):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)
def fill_task(driver, message):
    question = driver.find_element_by_id('question')
    time.sleep(3)
    write_something_normally(message, question, 0.1)
    time.sleep(1)
    question.send_keys(Keys.ENTER)

def fill_email(driver, email):
    email_form = driver.find_element_by_id('email')
    time.sleep(3)
    write_something_normally(email, email_form, 0.1)
    time.sleep(1)
    email_form.send_keys(Keys.ENTER)

def fill_comments(driver, comments):
    comments_form = driver.find_element_by_id('comments')
    time.sleep(3)
    write_something_normally(comments, comments_form, 0.01)
    time.sleep(1)
    comments_form.send_keys(Keys.ENTER)

def send_it(driver):
    driver.find_element_by_id('submit').click()

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    open_bob(driver)
    fill_task(driver, "Send personalized emails to all L2L students")
    fill_email(driver, "gabriel.bstd@gmail.com")
    details = "Here is my google spreadsheet with all the email addresses : https://docs.google.com/spreadsheets/d/1TFFDgkKY4Iig6Ggt9uRNuE_tyuau-dUPEgWbhnHblf0/edit#gid=0"
    details2 = "Here is my message:\nDear NAME,\nINTRO\nI hope everything is doing well at STARTUP\n\nCheers!\nGab"
    fill_comments(driver, details + "\n" + details2)
    send_it(driver)
