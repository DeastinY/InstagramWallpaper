from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import os

url = 'http://instagram.com'
user = '/wachmacher/'
imagefile = 'temp.jpg'

driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
driver.set_window_size(1120, 550)
driver.get(url+user)

soup = BeautifulSoup(driver.page_source, "lxml")

latest = soup.find('a')
alt = latest.find('img')['alt']
driver.get(url+latest['href'])
soup = BeautifulSoup(driver.page_source, "lxml")
img = None
for i in soup.findAll('img'):
    if i.get('alt') == alt:
        img = i
        break
urllib.request.urlretrieve(img.get('src'), imagefile)

absimg = os.path.abspath(imagefile)

if os.name == 'nt':
    import ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, absimg , 0)
elif os.name == 'posix':
    import subprocess
    status = subprocess.Popen("DISPLAY=:0 GSETTINGS_BACKEND=dconf "
             "/usr/bin/gsettings set org.gnome.desktop.background "
             "picture-uri file://"+absimg, shell=True)
    status.wait()
    if status.returncode != 0:
        print("Could not set desktop :( Probably your desktop environment is not supported.")

#os.remove(imagefile)
