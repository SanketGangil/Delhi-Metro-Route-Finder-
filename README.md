# DMRC Route Finder

A web-based **Delhi Metro Route Finder** that calculates the **best route** between two metro stations using graph-based algorithms.  
The application displays the **fare, estimated travel time, total stops**, and line interchanges through a simple and intuitive UI.

---

## Features

- Find the **best metro route** between any two stations
- Automatic **line change detection**
- Displays **estimated travel time**
- Calculates **fare**
- Shows **number of stops**
- Graph-based path computation
- Simple web interface using HTML templates

---

## Tech Stack

- **Backend:** Python (FastAPI / Starlette-style routing)
- **Algorithm:** Graph + Shortest Path logic
- **Frontend:** HTML, CSS (Jinja2 templates)
- **Data Source:** JSON-based Delhi Metro route data
- **Server:** Uvicorn

---

## Project Structure

```bash
DMRC_ROUTE_FINDER/
│
├── data/
│   └── metro_routes.json      # Delhi Metro stations & distances
│
├── static/
│   └── style.css              # Styling for UI
│
├── templates/
│   ├── index.html             # Home page (station selection)
│   └── result.html            # Route result display
│
├── main.py                    # Application entry point
├── metro_graph.py             # Graph creation & route logic
├── scrape.py                  # Script to scrape metro data
│
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── .gitignore
```
---


## Installation & Setup

- 1️. Clone the Repository
```bash
git clone https://github.com/SanketGangil/Delhi-Metro-Route-Finder-.git
cd Delhi-Metro-Route-Finder-
```

- 2️. Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

```bash
source venv/bin/activate #macOS / Linux
venv\Scripts\activate #Windows
```


- 3️. Install Dependencies
```bash
pip install -r requirements.txt
```

- Run the Application
```bash
uvicorn main:app --reload
```
- Open your browser and go to:
```bash
http://127.0.0.1:8000
```
---

## How It Works

* User selects source and destination metro stations

* Metro data is loaded from metro_routes.json

* Stations are converted into a graph structure

* A shortest-path algorithm computes the best route

* The UI displays:

* * Fare

* * Estimated travel time

* * Total stations

* * Line interchanges

---

## Output Details

- Fare: Estimated using station distance

- Time: Derived from cumulative distances

- Stops: Total stations in route

- Line Changes: Clearly highlighted