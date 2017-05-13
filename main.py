from seriesonline import seriesOnline as so
import json

try:
    conf = open("video_files.conf")
    files = json.loads(conf.read())["shows"]
except Exception as e:
    print "Error: "+ str(e)

s = so()

for show in files:
    s.setShow(show)
    s.start()
