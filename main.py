from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from metro_graph import MetroGraph

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

DATA_FILE = os.path.join("data", "metro_routes.json")
if os.path.exists(DATA_FILE):
    graph = MetroGraph.from_json(DATA_FILE)
else:
    graph = MetroGraph()

# Home Page (Form)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Renders the home page with the station dropdown.
    """
    stations = sorted(list(graph.adj.keys()))
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stations": stations
    })

#Results Page (Processing)
@app.post("/result", response_class=HTMLResponse)
async def result(
    request: Request,
    source: str = Form(...),      
    destination: str = Form(...) 
):
    """
    Handles form submission, runs logic, and renders result.
    """
    stations = sorted(list(graph.adj.keys()))

    # Validation
    if not source or not destination:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Please select both stations",
            "stations": stations
        })

    # Run Logic
    route_data = graph.dijkstra(source, destination)

    if not route_data:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "No route found!",
            "stations": stations
        })

    # Render Result
    return templates.TemplateResponse("result.html", {
        "request": request,
        "data": route_data,
        "source": source,
        "destination": destination
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)