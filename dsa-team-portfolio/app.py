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

if __name__ == '__main__':
    app.run(debug=True)