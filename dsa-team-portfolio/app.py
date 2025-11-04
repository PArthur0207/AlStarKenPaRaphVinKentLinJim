from flask import Flask, render_template
from backend.doubly_ended_queue import Queue

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

if __name__ == '__main__':
    app.run(debug=True)