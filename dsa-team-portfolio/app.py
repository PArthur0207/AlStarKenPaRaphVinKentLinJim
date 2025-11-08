from flask import Flask, render_template, send_from_directory
from backend import Queue
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
    contacts = [
        {"name": "Jimuel Ong", "github": "https://github.com/Gymwell19", "email": "ajimuelong@gmail.com", "facebook": "https://www.facebook.com/jimuel.ong.2025"},
        {"name": "James Starwin Canoy", "github": "https://github.com/Winstar-git", "email": "james.canoy87@gmail.com", "facebook": "https://www.facebook.com/jamesstarwin10"},
        {"name": "Kent Aj Rins", "github": "https://github.com/kenttyyy", "email": "kentajrins123@gmail.com", "facebook": "https://www.facebook.com/kent.aj.amora.rins"},
        {"name": "Kenneth Serrano", "github": "https://github.com/iskenneth", "email": "serranokenneth94@gmail.com", "facebook": "https://www.facebook.com/kenneth.gacos22"},
        {"name": "Vincent Aliling", "github": "https://github.com/vinci35p", "email": "vinsoyt4321@gmail.com", "facebook": "https://www.facebook.com/vinsoyt.ali.2424/"},
        {"name": "Linden Powell Rivera", "github": "https://github.com/lindenn21", "email": "lindenpowell218@gmail.com", "facebook": "https://www.facebook.com/lindenpowell.rivera"},
        {"name": "Paul Arthur Marayan", "github": "https://github.com/PArthur0207", "email": "marayanpaularthur1114@gmail.com", "facebook": "https://www.facebook.com/paularthur.marayan.92"},
        {"name": "Raphael Inducil", "github": "https://github.com/RaphaelInducil", "email": "clouieeraphael@gmail.com", "facebook": "https://www.facebook.com/raphael.inducil"},
        {"name": "Aldrin Paul Reyes", "github": "https://github.com/DrinQt", "email": "aldrinreyeslol694@gmail.com", "facebook": "https://www.facebook.com/Aldrin.Paul.Reyes14"},
    ]

    return render_template("contact.html", contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)