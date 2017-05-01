import json
import wget
import os
import time
from pyvirtualdisplay import Display
from selenium import webdriver
#condition handling
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#error checking
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

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
display = Display(visible=0, size=(800,600))
for show in files: #loops though all show files in conf
    display.start()
    print "Currently Downloading Episodes of " + show["name"] +" season "+show["season"]
    driver = webdriver.Chrome(chromedriver)
    #driver = webdriver.PhantomJS(phantomdriver)
    driver.set_page_load_timeout(5)#setting timeout error to stop pending requests
    wait = WebDriverWait(driver, 10)
    title = show["name"].lower().replace(" ","-")
    driver.get('https://seriesonline.io/movie/search/'+title)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ml-item")))
        print "Page with Season figures loads"
    except Exception as e:
        print "Error: "+ str(e)


    #find correct season
    try:
        driver.find_element_by_xpath('//div[@class="ml-item"]//a[contains(@href, "'+title+'-season-'+show["season"]+'")]').click()
    except TimeoutException:
        driver.execute_script("window.stop();")

    #go to episodes
    driver.find_element_by_xpath('//a[contains(@href, "watching")]').click()
    #find correct episode
    for ep in show["episodes"]:
        servereps = driver.find_elements_by_xpath('//a[contains(@title, "Episode '+ep+'")]')
        eTitle = show["name"].title() + " - Season " + show["season"] + " Episode " + ep + ".mp4" 
        try:
            servereps[0].click()
        except TimeoutException:
            driver.execute_script("window.stop();")
            

        #switch to iframe
        print "Switching to iframe"
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="media-player"]/div/iframe'))
        wget.download(driver.find_element_by_tag_name('video').get_attribute('src'), out=eTitle)
        print "Switching back to main page"
        driver.switch_to.default_content()
        



driver.quit()
display.stop()
