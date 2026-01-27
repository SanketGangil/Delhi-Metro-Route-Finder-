```sh
# 🚇 DMRC Route Optimization Engine

A high-performance web application that calculates the most efficient route between Delhi Metro stations using **Dijkstra’s Algorithm** and **FastAPI**. It optimizes for travel time by accounting for line interchanges and provides estimated fares and travel duration.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Algorithm](https://img.shields.io/badge/Algorithm-Dijkstra-orange)

## 🚀 Features

* **Smart Routing:** Uses a modified Dijkstra algorithm that penalizes line switching to find the *fastest* route, not just the shortest distance.
* **Condensed Path View:** Intelligently summarizes long routes to show only key stations (Start, Interchanges, End) for a cleaner UX.
* **Fare & Time Estimation:** Calculates ticket cost based on official DMRC distance slabs and estimates travel time including stoppage/interchange delays.
* **High Performance:** Built on **FastAPI** (Asynchronous) for sub-50ms response times.
* **Interactive API Docs:** Includes automatic Swagger UI documentation (`/docs`).

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Algorithm:** Graph Theory (Weighted Graph, Priority Queue)
* **Frontend:** Jinja2 Templates, HTML5, CSS3
* **Data:** JSON (Adjacency List structure), BeautifulSoup (Scraper)

## 📂 Project Structure

```text
/metro_project
├── main.py               # FastAPI Server & Routes
├── metro_graph.py        # Core Logic (Dijkstra & Fare Rules)
├── requirements.txt      # Dependencies
├── static/
│   └── style.css         # Styling
├── templates/
│   ├── index.html        # Search Page
│   └── result.html       # Result Page
└── data/
    └── metro_routes.json # Network Data
```