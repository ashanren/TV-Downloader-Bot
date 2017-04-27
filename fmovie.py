import json
import os
import time
from selenium import webdriver
#condition handling
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#error checking
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import wget

def popupHandler():
    #removal of popup
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        print "no popup appeared"

def openload():
    print "Gets to openload function"
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    pops = driver.find_element_by_id('videooverlay')
    pops.click()
    return driver.find_element_by_tag_name('video').get_attribute('src')
    #popupHandler()
    #pops.click()
    #time.sleep(1)
    #pops.click()
    #driver.switch_to.default_content()
    #driver.switch_to.frame(driver.find_element_by_xpath('//iframe[@webkitallowfullscreen="true"]'))
    #return driver.find_element_by_tag_name('video').get_attribute('src')

    
    #hopefully find the src of the video

    
    return "Hello There"
#phantomdriver = os.path.abspath('node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs')
chromedriver = os.path.abspath('chromedriver')
#os.environ["webdriver.phantomjs.driver"] = phantomdriver
os.environ["webdriver.chrome.driver"] = chromedriver
files = []
try:
    conf = open("video_files.conf")
    files = json.loads(conf.read())["shows"]
except Exception as e:
    print "Error: "+ str(e)

for show in files: #loops though all show files in conf
    print "Currently Downloading Episodes of " + show["name"] +" season "+show["season"]
    driver = webdriver.Chrome(chromedriver)
    #driver = webdriver.PhantomJS(phantomdriver)
    driver.set_page_load_timeout(10)#setting timeout error to stop pending requests
    driver.get('https://www.fmovies.io/search.html?keyword='+show["name"].replace(" ", "+"))
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "figure")))
        print "Page with Season figures loads"
    except Exception as e:
        print "Error: "+ str(e)

    objs = driver.find_elements_by_tag_name("figure")
    #error checking for invalid season
    #if len(objs) > int(show["season"]):
    #    print "Not a Valid Season"
    #    continue

    for obj in objs: #searching for correct season
        name = obj.find_element_by_tag_name('a').get_attribute('href')
        if 'season-'+show["season"] in name:
            try:
                driver.get(name)
            except TimeoutException:
                driver.execute_script("window.stop();")
            #obj.click()
            print "Correct Season found and Clicked"
            break

    for ep in show["episodes"]:
        try:
            print "Looking for more button"
            driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[4]/div/div[1]').click()
            popupHandler()
        except Exception as e:
            print "There is no more button"


        #clicks correct episode
        popupHandler()
        if len(ep) == 1:
            ep = '0'+ep
        try:
            driver.find_element_by_xpath('//li/a[contains(@href, "episode-'+ep+'")]').click()
        except TimeoutException:
            driver.execute_script("window.stop();")
        except NoSuchElementException:
            try:
                driver.find_element_by_xpath('//li/a[contains(@href, "episode-'+ep[1]+'")]').click()
            except TimeoutException:
                driver.execute_script("window.stop();")
        popupHandler()
        #download episode
        #trying to switch to iframe
        print "Attempting to switch to iframe"
        driver.switch_to.frame(driver.find_element_by_xpath('//iframe[@webkitallowfullscreen="true"]'))

        #checks to see if google video or openload
        try:
            link = driver.find_element_by_tag_name("video").get_attribute('src')
        except NoSuchElementException:
            link = openload()
        print "Link to Episode "+ep+"Found! : "
        print link

        print "Switching back to main page"
        driver.switch_to.default_content()
driver.quit
