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
        self.driver.set_page_load_timeout(15)
        self.wait = WebDriverWait(self.driver, 10)

    def start(self):
        print "Starting script downloading episodes of " + self.show["name"] + " season " + self.show["season"]
        title = self.show["name"].lower().replace(" ","-")
        #massive problems with this. Occasionally will hit timeout and everything else will go out of wack. Will need a solution for this
        try:
            self.driver.get('https://seriesonline.is/movie/search/'+title)
        except TimeoutException:
            print "Trying to bypass Timeout Exception"
            self.driver.execute_script("$(window.stop())")
        print "finished loading page"
        #try:
        #    self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ml-item")))
        #    print "Season figure loads"
        #except Exception as e:
        #    print "Error: "+ str(e)
    
        #popup handling
        print "attempting to handle initial popup"
        self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/span').click()
        self.popupHandler()
        #find correct season
        try:
            episode = self.driver.find_element_by_xpath('//div[@class="ml-item"]//a[translate(@oldtitle,"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="'+self.show["name"].lower()+' - season '+self.show["season"]+'"]')
            title = episode.get_attribute('oldtitle')
            episode.click()
            print title
        except TimeoutException:
            self.driver.execute_script("$(window.stop())")
        self.popupHandler()
        #go to episodes
        try:
            self.driver.find_element_by_xpath('//a[contains(@href, "watching")]').click()
        except TimeoutException:
            self.driver.execute_script("$(window.stop())")
	
	#episode list
	episodes = self.driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/div[7]/div[1]/div[2]/a')	
        #find correct episode
        for ep in self.show["episodes"]:
            if ep[0] == '0':
                ep = ep[1]

            #creates title
	    eTitle = title + " Episode " + ep + ".mp4" 
            #handles current issue with bar on the bottom of screen
            try:
                self.driver.find_element_by_xpath('//div[@class="thumb mvic-thumb"]').click()
                self.popupHandler()
            except Exception as e:
                print "Can't find picture"
            #clicks on proper episode
            if (len(episodes) - int(ep)) >= 0:
                episodes[len(episodes) - int(ep)].click()
            else:
		print "Invalid Episode"
		continue
                #self.driver.execute_script("return window.stop();")
            #switch to iframe
            print "Finding Video src"
	    print self.driver.current_url
            try:
                link = self.googleVid()
            except Exception as e:
                link = self.openload()
            #threading for multi downlaoding support. Need to add a limit of 3-4 downloads
            threading.Thread(target=self.downloadEpisode, args=(link,eTitle,)).start()
            print "Switching back to main page"
            self.driver.switch_to.default_content()

    def setShow(self, show):
        self.show = show
        print "Current show is " + self.show["name"]

    def close(self):
        self.driver.quit()
        #self.display.stop()

    def popupHandler(self):
        #removal of popup
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            print "no popup appeared"

    def googleVid(self):
        self.driver.switch_to.frame(self.driver.find_element_by_xpath('//iframe[1]'))
	try:
	    self.wait.until(EC.presence_of_element_located((By.XPATH, '//video[contains(@src,"google")]')))
	except Exception as e:
	    print "Jarel OR Deep Error: " + str(e)

        return self.driver.find_element_by_tag_name('video').get_attribute('src')
        print "Video src is from googledirector"

    def openload(self):
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
        print "Video src is from openload"

    def downloadEpisode(self,link,eTitle):
            print "Downloading " + eTitle
            wget.download(link, out="Downloads/Shows/" + eTitle)
            print ""
            print eTitle + " finished"
