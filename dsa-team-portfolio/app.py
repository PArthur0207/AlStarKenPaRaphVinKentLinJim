from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify
from backend import *
from backend.sorting_manager import SortingManager
import json
import os

app = Flask(__name__)
customer_queue = CustomerQueue()
tree_manager = BinaryTreeManager()
dict_search = DictionarySearch()
route_search = MetroMap()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/works')
def works():
    data_file = os.path.join(app.root_path, 'data', 'projects.json')
    works = []
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            works = json.load(f)
    except Exception:
        works = []
    return render_template('works.html', works = works)

@app.route('/queue', methods=["GET", "POST"])
def queue_page():
    if request.method == "POST":
        if "add_customer" in request.form:
            name = request.form["name"]
            state = request.form["state"]
            customer_queue.add_customer(name, state)
        elif "serve_customer" in request.form:
            customer_queue.serve_customer()
        return redirect(url_for("queue_page"))
    
    return render_template("queue.html", line=customer_queue.get_line())

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

@app.route('/tree', methods=["GET", "POST"])
def tree_page():
    message = None
    root_exists = tree_manager.tree.root is not None

    if request.method == "POST":    
        # Determine which action
        if "add_root" in request.form or "add_node" in request.form:
            # Add root or child
            value = request.form.get("root_value") or request.form.get("new_value")
            value = value.strip()
            if not value:
                message = "Please enter a valid value."
            elif not root_exists:
                message = tree_manager.add_node(None, None, value)
                root_exists = True
            else:
                parent = request.form.get("parent_value").strip()
                side = request.form.get("side")
                if not parent or not side:
                    message = "Please provide parent and side for the new node."
                else:
                    message = tree_manager.add_node(parent, side, value)

        elif "delete_node" in request.form:
            value = request.form.get("delete_value").strip()
            if not value:
                message = "Please enter a value to delete."
            else:
                message = tree_manager.delete_node_by_value(value)

        elif "search_node" in request.form:
            value = request.form.get("search_value").strip()
            if not value:
                message = "Please enter a value to search."
            else:
                message = tree_manager.search_node(value)

        elif "replace_node" in request.form:
            old_value = request.form.get("old_value").strip()
            new_value = request.form.get("new_value_replace").strip()
            if not old_value or not new_value:
                message = "Please provide both old and new values."
            else:
                    message = tree_manager.replace_node(old_value, new_value)

        elif "delete_all" in request.form:
            message = tree_manager.delete_all_nodes()
            root_exists = False


    return render_template(
        "tree.html",
        tree=tree_manager.tree.root,
        message=message,
        root_exists=root_exists
    )

@app.route("/dict_search", methods=["GET", "POST"])
def dictionary_page():
    result = None
    message = None
    words = None

    if request.method == "POST":
        action = request.form.get("action")
        word = request.form.get("word", "").strip()

        # Add word
        if action == "add":
            if word:
                message = dict_search.add_word(word)
            else:
                message = "Please enter a word to add."

        # Search word
        elif action == "search":
            if word:
                result = dict_search.search_word(word)
            else:
                result = {"found": False, "path": [], "error": "Please enter a word to search."}

        # Delete word
        elif action == "delete":
            if word:
                message = dict_search.delete_word(word)
            else:
                message = "Please enter a word to delete."

        # Show all words
        elif action == "all":
            words = dict_search.get_all_words()

        #Delete all
        elif action == "delete_all":
            message = dict_search.delete_all()

    return render_template(
        "dict_search.html",
        result=result,
        message=message,
        words=words,
        tree=dict_search.bst.root
    )

@app.route('/')
@app.route('/graph', methods=['GET', 'POST'])
def graph_view():
    # 1. Load station data for the sidebar and SVG rendering
    # We navigate to the 'data' folder relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stations_json_path = os.path.join(current_dir, 'data', 'stations.json')
    
    try:
        with open(stations_json_path, 'r') as f:
            stations_data = json.load(f)
    except FileNotFoundError:
        return "Error: stations.json not found in data folder.", 404

    route = None
    
    # 2. Handle the "Calculate Route" request
    if request.method == 'POST':
        start_node = request.form.get('start_station')
        end_node = request.form.get('end_station')
        
        # We use the BFS-powered logic from our backend to find the shortest path
        if start_node and end_node:
            route = metro_system.get_route(start_node, end_node)

    # 3. Render the page with the map and (if calculated) the route
    return render_template('graph.html', stations=stations_data, route=route)

# API Route (Optional): If you want to fetch routes via JavaScript without reloading
@app.route('/api/route', methods=['GET'])
def get_route_api():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({"error": "Missing start or end station"}), 400
        
    route = metro_system.get_route(start, end)
    return jsonify(route)

if __name__ == '__main__':
    # Set debug=True during development to see live changes
    app.run(debug=True, port=5000)

@app.route('/sorting-algo', methods=["GET", "POST"])
def sorting_algo():
    result = None
    if request.method == "POST":
        algorithm = request.form.get("algorithm", "bubble")
        size = int(request.form.get("size", 10))
        result = SortingManager.run_sort(algorithm, size)
    return render_template("sorting_algo.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port)