from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api = os.getenv("URL")

current_page = 1
start = 1
max_pages = 200
all_books = []
file = 'allbooks.json'

while True:
    url = f"{api}?page={current_page}"
    print(f"Scraping page {current_page}...")
    req = requests.get(url)
    current_page += 1
    data = req.json()
    if not data['data']:
       print("No more data to scrape.")
       break
    data = json.dumps(data, indent=4)
    formatted_data = []
    for book in data['data']:
       name = book['name']
       author = book['authors'] 
       stock = book['stock']
       price = book['sales_price']
       formatted_data.append({
           'name': name,
           'author': author,
           'stock': stock,
           'price': price
       })
    try:
       with open(file, 'a', encoding='utf-8') as f:
           f.write(formatted_data)
    except Exception as e:
       print(f"An error occurred: {e}")
        
