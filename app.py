from flask import Flask, render_template, request
from metro_graph import MetroGraph
import os

app = Flask(__name__)

# SETUP
DATA_FILE = os.path.join("data", "metro_routes.json")
if os.path.exists(DATA_FILE):
    graph = MetroGraph.from_json(DATA_FILE)
else:
    graph = MetroGraph()

# ROUTE 1: Home Page (Form)
@app.route('/')
def index():
    # We need the list of stations for the dropdown
    stations = sorted(list(graph.adj.keys()))
    return render_template('index.html', stations=stations)

# ROUTE 2: Results Page (Processing)
@app.route('/result', methods=['POST'])
def result():
    # Getting data from the HTML Form
    source = request.form.get('source')
    destination = request.form.get('destination')

    if not source or not destination:
        return render_template('index.html', error="Please select both stations", stations=sorted(list(graph.adj.keys())))

    # Run Logic
    route_data = graph.dijkstra(source, destination)

    if not route_data:
        return render_template('index.html', error="No route found!", stations=sorted(list(graph.adj.keys())))

    # Rendering the Result Page with the data
    return render_template('result.html', data=route_data, source=source, destination=destination)

if __name__ == '__main__':
    app.run(debug=True)