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

class tvBot():

    def __init__(self):
        self.show = {}
        self.chromedriver = os.path.abspath('chromedriver')
        os.environ["webdriver.chrome.driver"] = self.chromedriver
        #display = Display(visible=0, size=(800,600))
        #display.start()
        self.driver = webdriver.Chrome(self.chromedriver)
        self.driver.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.driver, 10)

    def start(self):
        print "beginning download"

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
            
    def setShow(self, show):
        self.show = show
        print "Current show is " + self.show["name"]

    def googleVid(self):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//iframe[1]'))
        return self.driver.find_element_by_tag_name('video').get_attribute('src')

    def openload(self):
        print "openload video"
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//iframe[1]'))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        pops = self.driver.find_element_by_id('videooverlay')
        pops.click()
        self.popupHandler()
        #not sure why i need to do this yet but w/e
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//iframe[1]'))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
        print self.driver.find_element_by_tag_name('video').get_attribute('src')
        return self.driver.find_element_by_tag_name('video').get_attribute('src')

    def downloadEpisode(self,link,eTitle):
            print "Downloading " + eTitle
            wget.download(link, out="Downloads/Shows/" + eTitle)
            print ""
            print eTitle + " finished"
