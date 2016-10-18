# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:07:58 2016

@author: gchenard
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException
import time

#%%
def SD_connect(driver, doc_type, from_date, to_date):
    SD_link='https://arcc-acclaim.sdcounty.ca.gov/search/SearchTypeDocType'
    driver.get(SD_link)
    driver.find_element_by_id('btnButton').click()
    driver.find_element_by_id('DocTypesDisplay-input').clear()
    driver.find_element_by_id('DocTypesDisplay-input').send_keys(doc_type)
    driver.find_element_by_id('DocTypesDisplay-input').send_keys(Keys.TAB)
    driver.find_element_by_id('DocTypesDisplay-input').send_keys(Keys.TAB)
    driver.find_element_by_id('RecordDateFrom').clear()
    driver.find_element_by_id('RecordDateFrom').send_keys(from_date)
    driver.find_element_by_id('RecordDateFrom').send_keys(Keys.TAB)
    driver.find_element_by_id('RecordDateTo').clear()
    driver.find_element_by_id('RecordDateTo').send_keys(to_date)
    driver.find_element_by_id('btnSearch').submit()
    time.sleep(10)
    print (time)
    infos = {}
    print (infos)
    infos['Page 1'] = driver.find_element_by_tag_name('table').find_element_by_tag_name('tbody').driver.find_elements_by_tag_name('tr').driver.find_elements_by_tag_name('td').text
#    infos['Record Date'] = driver.find_element_by_class_name('formInput').text
    print (infos)
    return infos
#%%


#%%
driver = webdriver.Chrome()
SD_connect(driver,'DEED OF TRUST (007)', '10/1/2016', '10/13/2016')
