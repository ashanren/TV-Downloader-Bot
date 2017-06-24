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
class pelispedia(seriesOnline):
    
    def __init__(self):
        seriesOnline.__init__(self)

    def start(self):
        print "Pelispedia searching for " + self.show["name"] + " season " + self.show["season"]
        for ep in self.show["episodes"]:
            self.driver.get("http://pelispedia.net/" + self.show["name"].lower().replace(" ", "-") + "/" + self.show["season"] + "-sezon-" + ep + "-bolum.html") 

    def close(self):
        bot.close(self)
    def downloadEpisode(self, link, eTitle):
        bot.downloadEpisode(self, link, eTitle)
    def popupHandler(self):
        bot.popupHandler(self)
    def setShow(self, show):
        bot.setShow(self, show)
    def googleVid(self):
        bot.googleVid(self)
    def openload(self):
        bot.openload(self)


