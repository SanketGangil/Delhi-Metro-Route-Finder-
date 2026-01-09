```sh
# DMRC Smart Route Finder

A full-stack web application that calculates the most efficient route between Delhi Metro stations using **Dijkstra’s Algorithm**. It optimizes for travel time by accounting for line interchanges and provides estimated fares and travel duration.

## Features

* **Smart Routing:** Uses a modified Dijkstra algorithm that penalizes line switching to find the *fastest* route, not just the shortest distance.
* **Condensed View:** Intelligently summarizes long routes to show only key stations (Start, Interchanges, End).
* **Fare & Time Estimation:** Calculates ticket cost based on official DMRC distance slabs and estimates travel time including stoppage/interchange delays.
* **Interactive UI:** Modern, responsive interface with autocomplete for station names and visual timeline of the journey.
* **JSON Data Pipeline:** Custom scraper (BeautifulSoup) to build the graph network from raw DMRC data.

## Tech Stack

* **Backend:** Python, Flask
* **Algorithm:** Graph Theory (Dijkstra with Priority Queue)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Data:** JSON (Adjacency List structure)

## Project Structure

```text
/metro_project
├── app.py                # Flask Server & API Endpoints
├── metro_graph.py        # Core Logic (Dijkstra & Fare Rules)
├── requirements.txt      # Python Dependencies
├── static/
│   └── style.css         # Styling
├── templates/
│   ├── index.html        # Search Page
│   └── result.html       # Condensed Route View
└── data/
    └── metro_routes.json # Network Data
```