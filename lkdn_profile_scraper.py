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
#%%
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
    print(infos)

#%%
driver = webdriver.Firefox()
linkedin_connect(driver, 'h2464358@mvrht.com','Azerty')
get_profile_info(driver, 'https://www.linkedin.com/in/warren-chandler-622b78a')



driver.find_element_by_id('login-email').clear()
driver.find_element_by_id('login-email').send_keys('h2108596@mvrht.com')
driver.find_element_by_id('login-password').clear()
driver.find_element_by_id('login-password').send_keys('azedsqazedsq')
driver.find_element_by_id('login-submit').click()

#html=driver.page_source
#soup=BeautifulSoup(html)
url='https://www.linkedin.com/vsearch/p?title=CIO&openAdvancedForm=true&titleScope=CP&locationType=Y&f_G=us%3A0&f_I=14&rsid=5254215521475780977923&orig=ADVS&page_num='
driver.get(url + '1')
result_count = int(driver.find_element_by_id('results_count').text.split(' ')[0].replace(',',''))
nb_pages = math.ceil(result_count/10)
url_profiles=[]
start = time.time()

for i in range(nb_pages):
    print(i)
    driver.get(url + str(i+1))
    while True:
        try:
            a=driver.find_element_by_id('results').find_elements_by_class_name('result')
            break
        except:
            print('failed')
            pass
    for guy in a:
        guy_url = guy.find_element_by_class_name('result-image').get_attribute('href')
        url_profiles.append(guy_url)

print('It took ' + str((time.time() - start)/1000) + ' seconds!')

