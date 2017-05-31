# TV-Downloader-Bot

Application to download tv shows and movies.

Fmovie is operational.

Seriesonline is operational.

Sezonlukdizi initial commit. Not operational.

Pelispedia initial commit. Not operational.

# Core Dependencies

-pip

-Node.js

# Installation Instructions

1. Install python 2.7 and pip

2. Download Current version of Nodejs and NPM

3. Download and extract this repository, or use `git clone https://github.com/ashanren/TV-Downloader-Bot.git`

4. Use the commands `npm install` to install Node.js dependencies and `pip install -r requirements.txt` to install pip dependencies.

5. Download latest version of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/ "ChromeDriver Website") 

6. Install Xvfb `sudo apt-get install Xvfb`

# Usage Instructions

Go into `video_files.conf` There is a sample of the format this file should be in. Type in the name of the show, season, and episodes you want to download from that season. Copy and paste That general format to download multiple seasons. Make sure to keep this file in json format. Once finished type python main.py to start downloading. Headless functionality currently only works on Linux.
