from selenium import webdriver
#%%
def linkedin_connect(driver, username, password):
    linkedin_link='https://www.linkedin.com/'
    driver.get(linkedin_link)
    
    
    
    driver.find_element_by_id('login-email').clear()
    driver.find_element_by_id('login-email').send_keys(username)
    driver.find_element_by_id('login-password').clear()
    driver.find_element_by_id('login-password').send_keys(password)
    driver.find_element_by_id('login-submit').click()

def get_profile_info(driver, url):
    driver.get(url)
    infos = {}
    infos['name'] = driver.find_element_by_class_name('full-name').text
    infos['title'] = driver.find_element_by_class_name('title').text
    infos['current_employer'] =  driver.find_element_by_id('overview-summary-current').find_element_by_tag_name('td').find_element_by_tag_name('a').text
    infos['previous_employer'] =  driver.find_element_by_id('overview-summary-past').find_element_by_tag_name('td').find_element_by_tag_name('a').text
    infos['colleges']=[]    
    colleges = driver.find_element_by_id('background-education').find_elements_by_class_name('editable-item')
    for college in colleges:
        college_infos = {}
        college_infos['college_name'] = college.find_element_by_class_name('summary').text
        college_infos['degree'] = college.find_element_by_class_name('degree').text
        college_infos['major'] = college.find_element_by_class_name('major').text

        times = college.find_element_by_class_name('education-date').find_elements_by_tag_name('time')
        college_infos['starting_date'] = times[0].text
        college_infos['ending_date'] = times[1].text[2::]
        infos['colleges'].append(college_infos)
    infos['profile_link'] = url
    return(infos)

#%%
driver = webdriver.Firefox()
linkedin_connect(driver, 'h2558600@mvrht.com','azedsq')
print(get_profile_info(driver, 'https://www.linkedin.com/in/warren-chandler-622b78a'))
