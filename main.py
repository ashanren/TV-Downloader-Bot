from seriesonline import seriesOnline as so
from sezonlukdizi import sezonlukdizi as sld
#from watch5s import watch5s as ws
import json
import os

#create output Directories
if not os.path.exists(os.path.abspath('Downloads')):
    print "No Download Directory. Creating it"
    os.makedirs(os.path.abspath('Downloads'))
    os.makedirs(os.path.abspath('Downloads/Shows'))
    os.makedirs(os.path.abspath('Downloads/Movies'))
#open json
try:
    conf = open("video_files.conf")
    files = json.loads(conf.read())["shows"]
except Exception as e:
    print "Error: "+ str(e)

s = so()
#sd = sld()
#w = ws()

for show in files:
    s.setShow(show)
    s.start()
s.close()
