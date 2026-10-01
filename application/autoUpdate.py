from scraper import scrape_books
from compare import compare_and_update

if __name__ == "__main__":
   Succes = scrape_books()
   compare_and_update()
   print("Scraping and comparison completed.")