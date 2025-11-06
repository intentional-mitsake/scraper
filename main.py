from deepdiff import DeepDiff
import json
from scaper import scrape_books
from datetime import datetime

#first we scrape_books and write to the scraped json files
#scrape_books()
#then wwe compare the scraped json files with the existing allbooks.json and details.json files
#update the resultinng differences to the added and removed json files
#then we overwrite the allbooks.json and details.json files with the scraped json files and clear the scraped json files for next use
# and also every time we add new data to added and removed json files, we append to them instead of overwriting them and add a date

date = datetime.now().date()
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
        
        #ingore_order to avoid false positives due to different ordering of the items
        diff_allbooks = DeepDiff(allbooks, scrapedbooks, ignore_order=True)
        diff_details = DeepDiff(existing_details, scrapeddetails, ignore_order=True)
        
        #deepdiff returns a dictionary with different types of changes
        #we get 'iterable_item_added' and 'iterable_item_removed' and 'values_changed' if any
        added_books = diff_allbooks.get('iterable_item_added', {})
        removed_books = diff_allbooks.get('iterable_item_removed', {})
        print("Added Books:", added_books)
        print("Removed Books:", removed_books)

        with open('jsons/added.json', 'a', encoding='utf-8') as f:
            #first check if there are any added books
            if added_books:
                f.write(str(date) + '\n')
                for key, value in added_books.items():
                    f.write(json.dumps({key: value}, indent=4) + '\n')
        with open('jsons/removed.json', 'a', encoding='utf-8') as f:
            if removed_books:
                f.write(str(date) + '\n')
                print(removed_books)
                for key, value in removed_books.items():
                    f.write(json.dumps({key: value}, indent=4) + '\n')

       
    except Exception as e:
        print(f"An error occurred during comparison and update: {e}")

compare_and_update()