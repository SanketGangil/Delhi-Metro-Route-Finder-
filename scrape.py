import requests               
from bs4 import BeautifulSoup
import json                   
import os                     

def scrape_metro_routes():
    url = "https://delhimetrorail.info/delhi-metro-stations"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
 
    sections = soup.find_all('section') # lines are in section tag

    metro_routes = []  # List of dicts: [{line, branch_name, stations: [(name, dist)]}, ...]
    line_count = {}

    for section in sections:
        caption = section.find('caption') # gives me line name and table is inside it
        if not caption:
            continue

        line_name = caption.get_text(strip=True)

        # Track how many branches for each line
        count = line_count.get(line_name, 0) + 1
        line_count[line_name] = count
        branch_name = f"{line_name} - Branch {count}"

        rows = section.find_all('tr')[1:] # coz i wanna skip heding of table

        stations = []
        for row in rows:
            tds = row.find_all('td')
            if len(tds) >= 3:
                station_td = tds[1]  #  station name
                dist_td = tds[2]     #  distance 

                a_tag = station_td.find('a')
                if not a_tag:
                    continue

                station_name = a_tag.get_text(strip=True)

                # Safely extract first value only 
                # as the <td> is nested we use .contents and not .get_text
                dist_text = dist_td.contents[0].strip() if dist_td.contents else "0.0"

                try:
                    distance = float(dist_text)
                except ValueError:
                    print(f"Invalid distance for {station_name}: '{dist_text}'")
                    distance = 0.0

                stations.append((station_name, distance))

        if stations:
            metro_routes.append({
                "line": line_name,
                "branch": branch_name,
                "stations": stations
            })

    return metro_routes

#this saves scraped data into data/metro_routes.json.
def save_routes_to_file(routes, filename="data/metro_routes.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(routes, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(routes)} metro branches to '{filename}'.")

if __name__ == "__main__":
    routes = scrape_metro_routes()
    save_routes_to_file(routes)
