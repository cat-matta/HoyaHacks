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
path = "./youtube_comments.csv"
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

print("=" * 40)  # Shows in terminal when youtube summary page with search keyword is being scraped
print("Scraping " + link)    

sleep(5)
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

# create data frame to store as csv
df = pd.DataFrame(columns = ['url', 'title', 'channel', 'no_of_views', 'time_uploaded', 'comment', 'author', 'comment_posted', 
    'no_of_replies','upvotes','downvotes'])

# loop through each video
videocounter = 0
for url in urls:
    driver.get(url)
    v_channel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#upload-info yt-formatted-string"))).text
    print("channel name is ",v_channel)    
    v_views = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count span.view-count"))).text
    print("no. of views is ",v_views)
    v_timeUploaded = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string"))).text
    print("time uploaded is ",v_timeUploaded)

    # retrieve comments
    youtube_dict ={}


    print("+" * 40)  # Shows in terminal when details of a new video is being scraped
    print("Scraping child links ")
    #scroll down to load comments
    driver.execute_script('window.scrollTo(0,390);')

    # let comments load
    time.sleep(5)

    #sort by top comments
    print("sorting by top comments")
    sort= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#icon-label")))
    sort.click()
    
    topcomments =driver.find_element_by_xpath("""//*[@id="menu"]/a[1]/paper-item/paper-item-body/div[1]""")
    topcomments.click()
    sleep(3)

    # Loads 20 comments , scroll two times to load next set of 40 comments. 
    for i in range(0,2):
        driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight))")
        print("scrolling to load more comments")
        time.sleep(10)

    #count total number of comments and set index to number of comments if less than 50 otherwise set as 50. 
    totalcomments= len(driver.find_elements_by_xpath("""//*[@id="content-text"]"""))
    

    if totalcomments < 50:
        index= totalcomments
    else:
        index= 50 
    
    # loop through each comment and scrape info
    print("scraping through comments")
    ccount = 0
    while ccount < index: 
        try:
            comment = driver.find_elements_by_xpath('//*[@id="content-text"]')[ccount].text
        except:
            comment = ""
        try:
            authors = driver.find_elements_by_xpath('//a[@id="author-text"]/span')[ccount].text
        except:
            authors = ""
        try:
            comment_posted = driver.find_elements_by_xpath('//*[@id="published-time-text"]/a')[ccount].text
        except:
            comment_posted = ""
        try:
            replies = driver.find_elements_by_xpath('//*[@id="more-text"]')[ccount].text                    
            if replies =="View reply":
                replies= 1
            else:
                replies =replies.replace("View ","")
                replies =replies.replace(" replies","")
        except:
            replies = ""
        try:
            upvotes = driver.find_elements_by_xpath('//*[@id="vote-count-middle"]')[ccount].text
        except:
            upvotes = ""

        youtube_dict['url'] = url
        youtube_dict['link_title'] = titles[videocounter]
        youtube_dict['channel'] = v_channel
        youtube_dict['no_of_views'] = v_views
        youtube_dict['time_uploaded'] = v_timeUploaded
        youtube_dict['comment'] = comment
        youtube_dict['author'] = authors
        youtube_dict['comment_posted'] = comment_posted
        youtube_dict['no_of_replies'] = replies
        youtube_dict['upvotes'] = upvotes
        writer.writerow(youtube_dict.values())
        
        # increment comment counter
        ccount = ccount + 1
    # counter for the videos
    videocounter = videocounter+1