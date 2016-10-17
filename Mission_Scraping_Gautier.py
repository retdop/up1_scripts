# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 09:59:21 2016

@author: gchenard
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.common.exceptions import TimeoutException
import time

#%%
def Get_to_table(driver,url):
    driver.get(url)
    url2='http://acrparis.sbcounty.gov/cgi-bin/odsmnu1.html/input'
#    print (url2)    
    driver.get(url2)    
    url3='http://acrparis.sbcounty.gov/cgi-bin/Osearchc.mbr/input'
    driver.get(url3)   
    el = driver.find_element_by_name('Class')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == 'Deed of Trust':
            option.click() # select() in earlier versions of webdriver
            break
    driver.find_element_by_name('B1').submit() 
    print('got to table')
#%%    
def Enter_Date(driver, F_Month, F_Day, F_Year, T_Month, T_Day, T_Year):
#    driver.find_element_by_name('Class').select_by_value('0005').click()    
    driver.find_element_by_name('F_Month').send_keys(F_Month)
    driver.find_element_by_name('F_Month').send_keys(Keys.TAB)    
    driver.find_element_by_name('F_Day').send_keys(F_Day) 
    driver.find_element_by_name('F_Day').send_keys(Keys.TAB)    
    driver.find_element_by_name('F_Year').send_keys(F_Year)
    driver.find_element_by_name('F_Year').send_keys(Keys.TAB)    
    driver.find_element_by_name('T_Month').send_keys(T_Month)
    driver.find_element_by_name('T_Month').send_keys(Keys.TAB)    
    driver.find_element_by_name('T_Day').send_keys(T_Day)  
    driver.find_element_by_name('T_Day').send_keys(Keys.TAB)    
    driver.find_element_by_name('T_Year').send_keys(T_Year)
    driver.find_element_by_name('B1').submit()        
    print('date entered') 
#%%
def First_Link_Clicker(driver):
    first_doc_number=str(driver.find_element_by_tag_name('a').text)    
#    print (first_doc_number)    
    link_first_page=driver.find_element_by_link_text(first_doc_number)
#    print (link_first_page)
    link_first_page.click()
    print('clicked on 1st link')
#%%
def Get_doc_info(driver):
    doc_infos_temp = {}
    infos = driver.find_elements_by_tag_name('tr')
    info=infos[0].find_elements_by_tag_name('td')
#    print (info)    
    a=info[0].text        
   # print (a)
    i=0    
    for element in info:
        doc_infos_temp[i]=element.text     
        i+=1
    
   # print (doc_infos_temp)
    
    doc_info={}
    doc_info['Document Number']=doc_infos_temp[7]
    doc_info['Document Date']=doc_infos_temp[9]
    doc_info['Parcel Number']=doc_infos_temp[19]
    doc_info['Grantor Name']=doc_infos_temp[22]
    doc_info['Grantee Name']=doc_infos_temp[23] + doc_infos_temp[25]
    print (doc_info)
#%%
def Scrape_Website(driver,url):    
    
    Get_to_table(driver,url)    
    
    Enter_Date(driver, '01', '01', '2016','01', '10', '2016')
    
    First_Link_Clicker(driver)
    
    Get_doc_info(driver)
    
#%%
#class CygwinFirefoxProfile(webdriver.Firefox.firefox_profile):
#    @property
#    def path(self):
#        path = self.profile_dir
#        # Do stuff to the path as described in Jeff Hoye's answer
#        return path
##%%
#driver = webdriver.Firefox(firefox_profile=CygwinFirefoxProfile())

url='http://acrparis.sbcounty.gov'
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')    
Scrape_Website(driver,url)