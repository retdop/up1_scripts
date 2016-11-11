import math
import os
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


#company name,
# profit,
# #followers,
# duration,
# amount raised 
#and website



def go_to_website(driver, url, xpath):
    driver.get(url)
    WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.XPATH, xpath))
    )

#%%

def scrape_companies(driver, companies_infos):
#    profiles_info_file = open('profiles_info1.txt', 'w')
#    count = 0
#    success_count = 0
    
    lis = driver.find_elements_by_xpath('/html/body/section[3]/div/div/div/ul/li')
    #company name,
# profit,
# #followers,
# duration,
# amount raised 
#and website
    for li in lis:
        comp={}
#        try:
        comp['name'] = li.find_element_by_xpath('div/div/h6').text
        comp['profit'] = li.find_element_by_xpath('div/div/div[2]/div/p/span').text
        comp['followers'] = li.find_element_by_xpath('div/div/div[3]/div[1]/p/span').text
        comp['duration'] = li.find_element_by_xpath('div/div/div[3]/div[2]/p/span').text
        comp['raised'] = li.find_element_by_class_name('funded').find_element_by_tag_name('strong').text
        comp['url'] = li.find_element_by_xpath('div/a').get_attribute('href')
#        except:
#            print('fuck')
        companies_infos.append(comp)
    return(companies_infos)
#%%
import csv
def dicts_to_csv(filename, list_of_dicts, keys):
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)
#%%
if __name__=='__main__':

    os.chdir('/home/gabriel/xberkeley/up1/up1_scripts/')

    companies_infos = []
    driver = webdriver.Firefox()
    for i in range(7):
        go_to_website(driver, 'https://www.kickfurther.com/coops/funded?page=' + str(i+1), '/html/body/section[1]/div/div/h1')
        companies_infos = scrape_companies(driver, companies_infos)
    for company in companies_infos:
        go_to_website(driver, company['url'], '/html/body/section[1]/div/div/div[1]/h1')
        company['website'] = driver.find_element_by_xpath('/html/body/section[1]/div/div/div[1]/p[2]/a').get_attribute('href')

    keys = ['name', 'profit','followers', 'duration', 'raised', 'website', 'url']
    dicts_to_csv('profiles_info1.csv', companies_infos, keys)
