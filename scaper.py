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
all_books = 'jsons/scrapedbooks.json'
detailed_file = 'jsons/scrapedDetails.json'


#filters
genreFilter = ["fiction-and-literature", "history-biography-and-social-science"]
subGenreFilter = ["classics", "fantasy", "science-fiction","mystery-thriller-and-suspense", "historical-fiction", "contemporary"]

def scrape_books(genreFilter=genreFilter, subGenreFilter=subGenreFilter):  
    #to initialize the json files with an opening bracket
    try:
        #first use 'w' mode to overwrite any existing data
        with open(all_books, 'w', encoding='utf-8') as f:
            f.write('[')  # start of json array
                        
        with open(detailed_file, 'w', encoding='utf-8') as fd:
            fd.write('[')  # start of json array
    except Exception as e:
        print(f"An error occurred: {e}")
    # so we iterate through all genres and sub-genres and scrape data accordingly
    # genre headers to separte them in the files
    for genre in genreFilter:
        if genre == "history-biography-and-social-science":
            #so that we only scrape the relevant/existing sub-genre for this genre
            subGenreFilter = ["history"]
        for sub_genre in subGenreFilter:
            #the for loop will run once for each sub_genre
            #each iteration for each sub_genre will have its own while loop to go through all the pages of that sub_genre

            #new lists for each sub_genre to avoid data overlap
            initial = []
            names = []

            #reset current_page to start at the beginning of each sub_genre
            current_page = start
            while True:
                #for fiction and literature
                url = f"{api}?genre={genre}&sub_genres={sub_genre}&page={current_page}" 
                #for history
                #url = f"{api}?genre={genreFilter[1]}&sub_genres=history&page={current_page}"
                print(f"Scraping {sub_genre} page {current_page}...")
                req = requests.get(url)
                current_page += 1
                data = req.json()
                #if there is no more data, break the loop as that means we have reached the end
                if not data['data']:
                    print("No more data to scrape.")
                    # then we format the data in respect to sub_genre and add a total count for each sub_genre 
                    # & write to the json files
                    formatted_data = {
                        'Genre': sub_genre,
                        'Total Books': len(names),
                        'Books': names
                    }
                    detailed_data = {
                        'Genre': sub_genre,
                        'Total Books': len(initial),
                        'Books': initial
                    }
                    #clear the initial list for next sub_genre
                    #initial.clear()
                    #names.clear()
                    #as we are creating new lists for each sub_genre, no need to clear them
                    try:
                        #with closes the file after writing
                        with open(all_books, 'a', encoding='utf-8') as f:
                                #to convert dict(item) to string
                                #can only write strings to a file
                                #f.write(item.__str__() + '\n')
                                # this is to format the json data properly with indents and new lines
                                json.dump(formatted_data, f, indent=4)
                                #history is the last sub_genre, so no need to add a comma after its json object
                                if(sub_genre != "history"):
                                   f.write(',\n')  # to add a new line after each json object
                        
                
                        with open(detailed_file, 'a', encoding='utf-8') as fd:
                                json.dump(detailed_data, fd, indent=4)
                                if(sub_genre != "history"):
                                    fd.write(',\n')
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    break

                # if there is data, proceed to extract relevant information
                #iterate through the data and extract relevant information only
                for book in data['data']:
                    name = book['name']
                    author = book['authors']
                    stock = book['stock']
                    price = book['sales_price']
                    # inital list will store the all extracted of each genre data 
                    initial.append({
                        'name': name,
                        'author': author,
                        'price': price
                    })
                    names.append(name)
    
    try:
        with open(all_books, 'a', encoding='utf-8') as f:
            f.write(']')  # start of json array
                        
        with open(detailed_file, 'a', encoding='utf-8') as fd:
            fd.write(']')  # start of json array
    except Exception as e:
        print(f"An error occurred: {e}")
    

        
