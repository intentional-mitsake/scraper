from flask import Flask, render_template, redirect, url_for
from scraper import scrape_books
from compare import compare_and_update
import json

app = Flask(__name__)

def load_json():
    try:
        with open('jsons/changes.json', 'r') as f:
            # return the loaded json data
            return json.load(f)
    except FileNotFoundError:
        return {"status": "Error", "last_message": "changes.json not found!"}
    except json.JSONDecodeError:
        return {"status": "Error", "last_message": "changes.json is improperly formatted."}


# Define a route for the home page
@app.route('/')
def home():
    changes = load_json()
    return render_template('index.html', changes=changes)

# Define a route to trigger scraping and comparison
@app.route('/update', methods=['POST'])
def scrape_and_compare():
    scrape_books()
    compare_and_update()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # run the Flask app
    app.run(debug=True)