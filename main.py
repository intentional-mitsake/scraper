from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("URL")

req = requests.get(url)
#check if the connection was successful first
if(req.status_code == 200):
    print("Connection Successful")
    html = req.text #getting the actual html content if the connection is successful
    soup = BeautifulSoup(html, 'html.parser')
    loadMoreTag = soup.find('div', class_= 'load-more book-filter__content__load-more')
    print(loadMoreTag)
else:
    print("Connection Failed with status code:", req.status_code)
    html = ""

