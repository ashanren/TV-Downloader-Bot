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
from bot import tvBot as bot

class fmovie(bot):
	
	def __init__(self):
		bot.__init__(self)

	def start(self):
		print "Fmovie searching for " + self.show["name"] + " season " + self.show["season"]

		self.driver.get('https://www.fmovies.io/search.html?keyword='+self.show["name"].replace(" ", "+"))
		try:
			self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "figure")))
			print "Initial Page loaded"
		except Exception as e:
			print "Jarel Error: " + str(e)
		#initial popup handling
		self.driver.find_element_by_xpath('/html/body/div/article[1]/h2').click()
		self.popupHandler()
		#loading correct season
		try:
			self.driver.find_element_by_xpath('//a[contains(@href, "'+self.show["name"].replace(" ", "-").lower()+'-season-'+self.show["season"]+'")]').click()
		except TimeoutException:
			print "Timeout Error activated"
			try:
				self.driver.execute_script("$(window.stop())")
			except Exception as e:
				print "Gets to the click trial"
				self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/div[2]/div[4]/a').click()
				print "Passes the click trial"
				#self.driver.execute_script("return window.stop();")
			print "Stopped error"
		except Exception:
			print "Invalid Season"
			return

		#optaining eTitle
		title = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/ul/li[3]').text.replace('"', '')
		print "basic title is : " + title

		for ep in self.show["episodes"]:
			if ep[0] == '0':
				ep = ep[1]
			#clicking more button
			try:
				self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[4]/div/div[1]').click()
				print "Clicked more button"
			except Exception as e:
				self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/div[2]/div[4]/a').click()
				print "Clicked lower more button"
			self.popupHandler()
			#loading correct episode
			#litle weird but i think it works
			episodes = self.driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[4]/div/ul/li')
			print "Finding episode " + str(len(episodes) - int(ep) + 1)
			#needs error checking here for invalid episodes
			try:
				episodes[len(episodes) - int(ep)].find_element_by_tag_name('a').click()
			except TimeoutException:
				self.driver.execute_script("$(window.stop())")
				print "Final error avoided"
			except Exception:
				print "Invalid Episode #"
				continue
			link = ''
			try:
				link = self.googleVid()
			except Exception as e:
				link = self.openload()

			eTitle = title + " Episode " + ep + ".mp4"
			threading.Thread(target=self.downloadEpisode, args=(link,eTitle,)).start()
			print "Switching back to main page"
			self.driver.switch_to.default_content()

	def close(self):
		bot.close(self)
	def downloadEpisode(self, link, eTitle):
		bot.downloadEpisode(self, link, eTitle)
	def popupHandler(self):
		bot.popupHandler(self)
	def setShow(self, show):
		bot.setShow(self, show)
	def googleVid(self):
		return bot.googleVid(self)
	def openload(self):
		return bot.openload(self)
