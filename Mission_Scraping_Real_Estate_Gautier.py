# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 09:59:21 2016

@author: gchenard
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.common.exceptions import NoSuchElementException
 
    
#%%
def Get_to_list(driver,url):
    driver.get(url)
    url2='http://acrparis.sbcounty.gov/cgi-bin/odsmnu1.html/input'
    driver.get(url2)    
    url3='http://acrparis.sbcounty.gov/cgi-bin/Osearchc.mbr/input'
    driver.get(url3)   
    print('got to list')
    
def Find_element_in_list(driver):   
    el = driver.find_element_by_name('Class')
    for option in el.find_elements_by_tag_name('option'):   #find the good element in the list
        if option.text == 'Deed of Trust':
            option.click()
            break
    driver.find_element_by_name('B1').submit() 
    print('element found in the list - got to table')
#%%    
def Enter_Date(driver, F_Month, F_Day, F_Year, T_Month, T_Day, T_Year):
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
    first_doc_number=str(driver.find_element_by_tag_name('a').text)    #find the number of the first doc
    link_first_page=driver.find_element_by_link_text(first_doc_number)   #find the link associated with this number
    link_first_page.click()   #click on the link
    print('clicked on 1st link')
#%%
def Get_doc_info(driver):
    doc_infos_temp = {}          #stores all the info of the page
    infos = driver.find_elements_by_tag_name('tr')  #tr elements
    info=infos[0].find_elements_by_tag_name('td')   #td elements insisde the first tr element
    
    i=0    
    for element in info:    #associate a number to each element of info (to identify Number, Date and Parcel that are always at the same emplacement)
        doc_infos_temp[i]=element.text     #store each of these element into doc_info_temp dictionary
        i+=1

    doc_info['Document Number']=doc_infos_temp[7]  #doc info is the dictionary that stores only the elements that we want (definied at the end of the program)
    doc_info['Document Date']=doc_infos_temp[9]
    doc_info['Parcel Number']=doc_infos_temp[19]
    
    grant_info=info[0].find_elements_by_tag_name('tr')   #find tr elements into the first tr element
    grant_info_bis= grant_info[11].find_elements_by_tag_name('td')  #grant info 11 being the table with grantor and grantee name
    count=1    
    doc_info['Grantor Name'] = [] 
    doc_info['Grantee Name'] = [] 
    for element in grant_info_bis:  #itterate through the table
        if count%2==0:
            doc_info['Grantor Name'].append(element.text)  #"even" elements of the table are Grantors
        elif count>1: 
            doc_info['Grantee Name'].append(element.text)  #"odd" elements of the table are Grantees, except the first one
        count+=1
    doc_info['Grantor Name']='; '.join(doc_info['Grantor Name'])   #converting the list of grantors into a more readable semi-colon separated value
    doc_info['Grantor Name']=doc_info['Grantor Name'].replace(';           ','') #deleting spaces when there is no name
    doc_info['Grantee Name']='; '.join(doc_info['Grantee Name'])     #same as up
    doc_info['Grantee Name']=doc_info['Grantee Name'].replace(';           ','')  #same as up

#%%


def Go_to_next_page(driver):
    try:
        z=driver.find_element_by_xpath("//img[contains(@src, 'nextdoc.gif')]/parent::a").click()
        return(True) 
    except NoSuchElementException:
        return(False)
        
    
#%%
def put_info_in_list(List_of_docs, doc_info):
    copy=doc_info.copy() 
    List_of_docs.append(copy)

#%%

def Convert_to_csv(List_of_docs):

    keys = ['Document Number', 'Document Date', 'Parcel Number', 'Grantor Name', 'Grantee Name']
    with open('real-estates-doc-1.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(List_of_docs)
       
#%%
def Scrape_Website(driver,url):    
    
    nb_pages_done =0
    
    Get_to_list(driver,url)

    Find_element_in_list(driver)    
        
    Enter_Date(driver, '01', '01', '2016','01', '10', '2016')
        
    First_Link_Clicker(driver)
    
    Get_doc_info(driver)
        
    put_info_in_list(List_of_docs,doc_info)
      
    while Go_to_next_page(driver):    
        
        Get_doc_info(driver)
        
        put_info_in_list(List_of_docs,doc_info)
        
        nb_pages_done+=1
        
        print ('Page', str(nb_pages_done), 'scrappée')
   
    Convert_to_csv(List_of_docs)

    return List_of_docs

#%%
start = time.time()
doc_info={}
List_of_docs=[]
nb_pages_done=0  
url='http://acrparis.sbcounty.gov'
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')    
Scrape_Website(driver,url)

print ('Et voici la magnifique liste: ')
print (List_of_docs)

print('It took ' + str((time.time() - start)/1000) + ' seconds!')

print('fin')