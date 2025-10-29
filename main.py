from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api = os.getenv("URL")

current_page = 1
start = 1
all_books = []
#json file to store the scraped data
all_books = 'jsons/allbooks.json'
detailed_file = 'jsons/details.json'

#filters
genreFilter = ["fiction-and-literature", "history-biography-and-social-science"]
subGenreFilter = ["classics", "fantasy", "science-fiction","mystery-thriller-and-suspense", "historical-fiction", "contemporary"]


while True:
    #for fiction and literature
    url = f"{api}?genre={genreFilter[0]}&sub_genres={subGenreFilter[5]}&page={current_page}" 
    #for history
    #url = f"{api}?genre={genreFilter[1]}&sub_genres=history&page={current_page}"
    print(f"Scraping page {current_page}...")
    req = requests.get(url)
    current_page += 1
    data = req.json()
    #if there is no more data, break the loop as that means we have reached the end
    if not data['data']:
       print("No more data to scrape.")
       break
    #data = json.dumps(data, indent=4)
    formatted_data = []
    #iterate through the data and extract relevant information only
    for book in data['data']:
       name = book['name']
       author = book['authors']
       author_name = author[0]['name'] 
       stock = book['stock']
       price = book['sales_price']
       formatted_data.append({
           'name': name,
           'author': author_name,
           'price': price
       })
    try:
       #with closes the file after writing
       with open(file, 'a', encoding='utf-8') as f:
                #to convert dict(item) to string
                #can only write strings to a file
                #f.write(item.__str__() + '\n')

                #using json.dump to write json data to file
                json.dump(formatted_data, f, indent=2)
    except Exception as e:
       print(f"An error occurred: {e}")
        
