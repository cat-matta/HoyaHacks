# import required libraries
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
import time
import os
import csv
import pandas as pd
import re
from math import ceil

# Create a new .csv file to write data
path = "./data/youtube_comments_bodyimage.csv"
csv_file = open(path,'w', encoding="UTF-8", newline="")
writer = csv.writer(csv_file)

# write header names
writer.writerow(
    ['url', 'link_title', 'channel', 'no_of_views', 'time_uploaded', 'comment', 'author', 'comment_posted', 
     'no_of_replies','upvotes','downvotes'])

# scrape search results
link = "https://www.youtube.com/results?search_query=covid"

# open chrome 
driver = webdriver.Chrome(executable_path='C:/WebDriver/bin/chromedriver.exe')
driver.get(link)
time.sleep(10)

print("=" * 40)  # Shows in terminal when youtube summary page with search keyword is being scraped
print("Scraping " + link)    
time.sleep(20)    

# scrape top 8 video URLS that pop up on search
video_list = driver.find_elements_by_xpath('//*[@id="video-title"]')

info = []
urls = []
titles = []
channels = []
no_of_views = []
upload_dates = []

# store URL and video title for videos
for video in video_list:
    urls.append(video.get_attribute('href'))
    titles.append(video.get_attribute('title'))
    print("scraped ", video.get_attribute('title'))

#######################################