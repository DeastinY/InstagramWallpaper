from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import os

url = 'http://instagram.com'
user = '/wachmacher/'
imagefile = 'temp.jpg'

driver = webdriver.PhantomJS()
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

if os.name == 'nt':
    import ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, os.path.abspath(imagefile) , 0)

#os.remove(imagefile)
