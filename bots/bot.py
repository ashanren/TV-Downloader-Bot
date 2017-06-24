import wget
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
import threading
#headless option
from selenium.webdriver.chrome.options import Options

class tvBot():

	def __init__(self):
		self.show = {}
		self.chrome_options = Options()
		#self.chrome_options.add_argument("--headless")
		self.chromedriver = os.path.abspath('chromedriver')
		os.environ["webdriver.chrome.driver"] = self.chromedriver
		self.driver = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=self.chrome_options)
		self.driver.set_page_load_timeout(30)
		self.wait = WebDriverWait(self.driver, 10)

	def start(self):
		print "beginning download"
	
	def close(self):
		self.driver.quit()

	def popupHandler(self):
		#removal of popup
		if len(self.driver.window_handles) > 1:
			#print "Number of tabs currently: " + len(self.driver.window_handles)
			print "popupHandler has problem"
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
		#self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
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
