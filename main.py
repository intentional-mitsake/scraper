from deepdiff import DeepDiff
import json
from scaper import scrape_books
from datetime import datetime

#first we scrape_books and write to the scraped json files
scrape_books()

#then wwe compare the scraped json files with the existing allbooks.json and details.json files
#update the resultinng differences to the added and removed json files
#then we overwrite the allbooks.json and details.json files with the scraped json files and clear the scraped json files for next use
# and also every time we add new data to added and removed json files, we append to them instead of overwriting them and add a date

#compare 
date = datetime.now()
def compare_and_update():

    try:
        #read existing data and load them
        with open('jsons/allbooks.json', 'r', encoding='utf-8') as f:
            allbooks = json.load(f)
        with open('jsons/scrapedbooks.json', 'r', encoding='utf-8') as f:
            scrapedbooks = json.load(f)
        
        with open('jsons/scrapedDetails.json', 'r', encoding='utf-8') as f:
            scrapeddetails = json.load(f)
        with open('jsons/details.json', 'r', encoding='utf-8') as f:
            existing_details = json.load(f)
        
        #compare the jsons
        #print(scrapedbooks)
        changes = {} #empty dict to hold changes & we can define the structure later
        for new_items in scrapedbooks:
            genre = new_items['Genre'] # genre name is in the Genre key and we iterate over each genre
            num_new = len(new_items['Books']) # the Books key contains a list of books
            old_items = next((item for item in allbooks if item['Genre'] == genre), None) # find the corresponding genre in old data
            num_old = len(old_items['Books'])
            added_books = set(new_items['Books']) - set(old_items['Books']) # books present in new but not in old so added
            removed_books = set(old_items['Books']) - set(new_items['Books']) # books present in old but not in new so removesd
            print(f"Comparing genre: {genre}") 
            changes[genre] = {
                    'num_old': num_old,
                    'num_new': num_new,
                    'added': list(added_books),
                    'removed': list(removed_books),
                    'num_added': len(added_books),
                    'num_removed': len(removed_books),
                    'tot_changes': num_new - num_old # this should match num_added - num_removed so we can verify
                
            }
            print(f"Changes for genre {genre} recorded.")
        
            
        with open('jsons/changes.json', 'r', encoding='utf-8') as f:
            prev_data = f.read()
            prev_data = prev_data.rstrip('\n]\n') # remove the last closing bracket for appending new data
        with open('jsons/changes.json', 'w', encoding='utf-8') as f:
            # we read the previous data and store it in prev_data
            # then we removed trailing '\n]\n' from prev_data
            # now we overwrite changes.json with the previous data without the closing bracket
            # ensuring proper json format when we append new data
            f.write(prev_data)
            # \"\"--> to insert quotes in the date key
            # without it the json will be invalid
            # this is the format finally:
            # [ {"Date": "2024-06-01 12:00:00"},
            #   {"history": {.....}, "fantasy": {....} , .... }
            # ]    
            # add comma before the new entry as we are appending to an existing list        
            f.write(',\n{' + f"\"Date\": \"{str(date)}\"" + '},\n') #date of comparison
            json.dump(changes, f, indent=4)
            f.write('\n]\n')
             
       #overwrite the existing allbooks.json and details.json files with the scraped data for next comparison
        with open('jsons/allbooks.json', 'w', encoding='utf-8') as f:
            json.dump(scrapedbooks, f, indent=4)    
        with open('jsons/details.json', 'w', encoding='utf-8') as f:
            json.dump(scrapeddetails, f, indent=4)

        #clear the scraped json files for next use
        with open('jsons/scrapedbooks.json', 'w', encoding='utf-8') as f:
            f.write('[]') # empty list      
        with open('jsons/scrapedDetails.json', 'w', encoding='utf-8') as f:
            f.write('[]') # empty list
       
    except Exception as e:
        print(f"An error occurred during comparison and update: {e}")
compare_and_update()

