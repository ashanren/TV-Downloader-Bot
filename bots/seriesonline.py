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

class seriesOnline():

	def __init__(self):
		self.show = {}
		self.chrome_options = Options()
		self.chrome_options.add_argument("--headless")
		self.chromedriver = os.path.abspath('chromedriver')
		os.environ["webdriver.chrome.driver"] = self.chromedriver
		self.driver = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=self.chrome_options)
		self.driver.set_page_load_timeout(30)
		self.wait = WebDriverWait(self.driver, 10)

	def start(self):
		print "Starting script downloading episodes of " + self.show["name"] + " season " + self.show["season"]
		title = self.show["name"].lower().replace(" ","-")
		#massive problems with this. Occasionally will hit timeout and everything else will go out of wack. Will need a solution for this
		#might have fixed this
		try:
			self.driver.get('https://seriesonline.is/movie/search/'+title)
		except TimeoutException:
			print "Trying to bypass Timeout Exception"
			self.driver.execute_script("$(window.stop())")
		print "finished loading initial page"
		#popup handling
		self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div/div[1]/span').click()
		self.popupHandler()
		print "initial popup handled"
		#find correct season
		try:
			episode = self.driver.find_element_by_xpath('//div[@class="ml-item"]//a[contains(translate(@oldtitle,"ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"),"'+self.show["name"].lower()+' - season '+self.show["season"]+'")]')
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
			if (len(episodes) - int(ep)) >= 0 :
				episodes[len(episodes) - int(ep)].click()
			else:
				print "Invalid Episode"
				continue
			#switch to iframe
			print "Finding Video src"
			try:
				link = self.googleVid()
			except Exception as e:
				link = self.openload()
			print link
			#threading for multi downlaoding support. Need to add a limit of 3-4 downloads
			threading.Thread(target=self.downloadEpisode, args=(link,eTitle,)).start()
			print "Switching back to main page"
			self.driver.switch_to.default_content()
		print "Finished " + title + " list" 

	def setShow(self, show):
		self.show = show
		print "Current show is " + self.show["name"]

	def close(self):
		self.driver.quit()

	def popupHandler(self):
		#removal of popup
		if len(self.driver.window_handles) > 1:
			self.driver.switch_to.window(self.driver.window_handles[-1])
			#print "multiple popups "
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
		#self.driver.switch_to.frame(self.driver.find_element_by_xpath('//iframe[1]'))
		#print "switch to initial iframe"
		self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
		#self.driver.switch_to.frame(self.driver.find_element_by_xpath('//iframe[1]'))
		print "gets to secondary iframe"
		try:
			self.driver.find_element_by_id('videooverlay').click()
		except Exception:
			print "this is the new storage source im guessing"
			return self.driver.find_element_by_tag_name('video').get_attribute('src')

		self.popupHandler()
		#not sure why i need to do this yet but w/e
		self.driver.switch_to.frame(self.driver.find_element_by_xpath('//iframe[1]'))
		self.driver.switch_to.frame(self.driver.find_element_by_tag_name('iframe'))
		return self.driver.find_element_by_tag_name('video').get_attribute('src')
		print "Video src is from openload"



	def downloadEpisode(self,link,eTitle):
		print "Downloading " + eTitle
		wget.download(link, out="Downloads/Shows/" + eTitle)
		print ""
		print eTitle + " finished"
