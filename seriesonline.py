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
import threading

class seriesOnline():

    def __init__(self):
        self.show = {}
        self.chromedriver = os.path.abspath('chromedriver')
        os.environ["webdriver.chrome.driver"] = self.chromedriver
        #display = Display(visible=0, size=(800,600))
        #display.start()
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.set_page_load_timeout(10)
        self.wait = WebDriverWait(self.driver, 10)

    def start(self):
        print "Starting script downloading episodes of " + self.show["name"] + " season " + self.show["season"]
        title = self.show["name"].lower().replace(" ","-")
        try:
            self.driver.get('https://seriesonline.io/movie/search/'+title)
        except TimeoutException:
            self.driver.execute_script("return window.stop();")
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ml-item")))
        #print "Season figure loads"
        except Exception as e:
            print "Error: "+ str(e)
    
        #popup handling
        self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/span').click()
        self.popupHandler()
        #find correct season
        try:
            episode = self.driver.find_element_by_xpath('//div[@class="ml-item"]//a[translate(@oldtitle,"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="'+self.show["name"].lower()+' - season '+self.show["season"]+'"]')
            title = episode.get_attribute('oldtitle')
            episode.click()
            print title
        except TimeoutException:
            self.driver.execute_script("return window.stop();")
        self.popupHandler()
    #go to episodes
        try:
            self.driver.find_element_by_xpath('//a[contains(@href, "watching")]').click()
        except TimeoutException:
            self.driver.execute_script("return window.stop();")
        #find correct episode
        for ep in self.show["episodes"]:
            #this line needs to be replaced prob
            servereps = self.driver.find_elements_by_xpath('//a[contains(@title, "Episode '+ep+'")]')
            if ep[0] == '0':
                eTitle = title + " Episode " + ep[1] + ".mp4" 
            else:
                eTitle = title + " Episode " + ep + ".mp4" 

            #main server streaming down
            #self.driver.find_element_by_xpath('//div[contains(text(),"Main server")]').click()
            #self.popupHandler()
            try:
                servereps[0].click()
            except TimeoutException:
                self.driver.execute_script("return window.stop();")
            except Exception as e:
                servereps[1].click()
            
            #moving to its own method for future use
            #switch to iframe
            print "Finding Video src"

            try:
                link = self.googleVid()
            except Exception as e:
                link = self.openload()
            threading.Thread(target=self.downloadEpisode, args=(link,eTitle,)).start()
            print "Switching back to main page"
            self.driver.switch_to.default_content()
        #self.driver.close()
        #self.display.stop()
    def setShow(self, show):
        self.show = show
        print "Current show is " + self.show["name"]

    def close(self):
        self.driver.quit()

    def popupHandler(self):
        #removal of popup
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            print "no popup appeared"

    def googleVid(self):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="media-player"]/div/iframe'))
        return self.driver.find_element_by_tag_name('video').get_attribute('src')

    def openload(self):
        print "openload video"
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="media-player"]/div/iframe'))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        pops = self.driver.find_element_by_id('videooverlay')
        pops.click()
        self.popupHandler()
        #not sure why i need to do this yet but w/e
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="media-player"]/div/iframe'))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        print self.driver.find_element_by_tag_name('video').get_attribute('src')
        return self.driver.find_element_by_tag_name('video').get_attribute('src')

    def downloadEpisode(self,link,eTitle):
            print "Downloading " + eTitle
            wget.download(link, out=eTitle)
            print ""
            print eTitle + " finished"
