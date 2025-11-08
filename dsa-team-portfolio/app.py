from flask import Flask, render_template, send_from_directory
from backend import Queue
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/works')
def works():
    return render_template('works.html')
@app.route('/queue')
def queue():
    return render_template('queue.html')

@app.route("/contact")
def contacts_page():
    data_file = os.path.join(app.root_path, 'data', 'team.json')
    contacts = []
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
    except Exception as e:
        print(f"Error loading contacts: {e}")
        contacts = []
    return render_template('contact.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)