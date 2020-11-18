import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.workout

workoutlist = ['chest','back','abs','leg','shoulder','dumbbell']
for workout in workoutlist:
    browser = webdriver.Chrome('/Users/goodjungjun/Desktop/chromedriver')
    browser.get('https://www.youtube.com/results?search_query={}+workout+at+home'.format(workout))
    time.sleep(3)
    soap = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    imgs = soap.select('#img')
    chests = soap.select('#video-title')
    for chest in chests:
        url = 'https://youtube.com' + chest['href']
        title = chest['title']
        video_url = chest['href'][9:]
        video_one = {'title':title,'url':url, 'type':workout, 'video_url':video_url}
        db.workout.insert_one(video_one)




# url = 'https://www.youtube.com/results?search_query=chest+workout+at+home'
# headers = {'User Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}
#
# response = requests.get(url, headers = headers)
# soap = BeautifulSoup(response.text, 'html.parser')
#
# print(soap)