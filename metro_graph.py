import json
import heapq
from collections import defaultdict
import itertools  # <--- NEW IMPORT

class MetroGraph:
    def __init__(self):
        # Adjacency List: { "StationName": [("Neighbor", distance, "LineColor"), ...] }
        self.adj = defaultdict(list)

    def add_edge(self, u, v, weight, line):
        """Connects two stations with distance and line info."""
        self.adj[u].append((v, weight, line))
        self.adj[v].append((u, weight, line))

    @classmethod
    def from_json(cls, filepath):
        """Loads data from the scraped JSON file."""
        graph = cls()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                routes = json.load(f)

            for route in routes:
                line = route["line"]
                stations = route["stations"]

                for i in range(len(stations) - 1):
                    u, dist_u = stations[i]
                    v, dist_v = stations[i + 1]
                    
                    # Distance between two adjacent stations
                    weight = abs(float(dist_v) - float(dist_u))
                    
                    if weight > 0:
                        graph.add_edge(u, v, weight, line)
            
            print(f"✅ Graph loaded: {len(graph.adj)} stations ready.")
            return graph
        except Exception as e:
            print(f"❌ Error loading JSON: {e}")
            return cls()

    def dijkstra(self, source, target):
        """Finds the best route avoiding unnecessary interchanges."""
        
        # Generate a unique number for every item pushed to the queue
        # This acts as a "Tie Breaker" so Python never compares the 'path' list
        unique_id = itertools.count() 
        
        # Priority Queue Structure: 
        # (cost, tie_breaker, current_station, current_line, path_history)
        pq = [(0, next(unique_id), source, None, [])]
        
        # Visited stores: (station, line_arrived_on) -> min_cost
        visited = {}

        while pq:
            # Unpack the 5 elements
            cost, _, current_node, curr_line, path = heapq.heappop(pq)

            state = (current_node, curr_line)
            if state in visited and visited[state] <= cost:
                continue
            visited[state] = cost

            # Add current step to path
            new_path = path + [{'station': current_node, 'line': curr_line}]

            # If destination reached
            if current_node == target:
                return self.calculate_metrics(cost, new_path)

            # Check neighbors
            for neighbor, weight, line in self.adj[current_node]:
                # Logic: If we change lines, add a 'Penalty'
                penalty = 0
                if curr_line is not None and line != curr_line:
                    penalty = 0.5 # Equivalent to adding 0.5km of "effort" to switch

                new_cost = cost + weight + penalty
                
                # Push with the new unique ID
                heapq.heappush(pq, (new_cost, next(unique_id), neighbor, line, new_path))

        return None

    def calculate_metrics(self, total_distance, path):
        """Calculates Fare (Rupees) and Time (Minutes)."""
        
        # 1. Fare Calculation (DMRC Slabs)
        d = total_distance
        fare = 0
        if d <= 2: fare = 10
        elif d <= 5: fare = 20
        elif d <= 12: fare = 30
        elif d <= 21: fare = 40
        elif d <= 32: fare = 50
        else: fare = 60

        # 2. Time Calculation
        stops = len(path)
        interchanges = 0
        
        # Count interchanges
        for i in range(1, len(path)):
            if path[i]['line'] != path[i-1]['line'] and path[i-1]['line'] is not None:
                interchanges += 1
        
        est_time = (d * 1.7) + (stops * 0.5) + (interchanges * 5)

        # Generate the condensed path
        condensed = self.get_smart_path(path)

        return {
            "total_distance": round(total_distance, 2),
            "stations_count": len(path), # Total stops (count full path)
            "interchanges": interchanges,
            "fare": fare,
            "estimated_time_mins": int(est_time),
            "path": condensed, # <--- RETURN THE SMART PATH HERE
            "full_path": path  # Keep full path if you ever need it for debugging
        }
    
    def get_smart_path(self, full_path):
        """
        Condenses a long path into just: Start -> Interchanges -> End.
        It adds context (previous/next station) around interchanges.
        """
        if not full_path:
            return []

        smart_path = []
        n = len(full_path)
        
        # Always add the starting station
        smart_path.append(full_path[0])

        for i in range(1, n - 1):
            prev_node = full_path[i-1]
            curr_node = full_path[i]
            next_node = full_path[i+1]

            # Detect Interchange: Line changes between previous and current
            # OR between current and next.
            prev_line = prev_node['line']
            curr_line = curr_node['line']
            next_line = next_node['line']

            is_interchange = (curr_line != prev_line) or (curr_line != next_line)
            
            # Context Logic: You asked to show "Rajiv Chowk (Blue) -> Rajiv Chowk (Yellow)"
            # My logic in 'dijkstra' already stores them as separate steps if the node is visited 
            # on different lines.
            
            # If it's an interchange, or the immediate neighbor of an interchange, we keep it.
            # But to keep it simple as per your request "Interchanges Only":
            
            if is_interchange:
                # Check if we already added this station (to avoid duplicates)
                if smart_path[-1]['station'] != curr_node['station']:
                    smart_path.append(curr_node)
                elif smart_path[-1]['line'] != curr_node['line']:
                    # Same station, different line (The explicit switch you wanted)
                    smart_path.append(curr_node)

        # Always add the destination
        if smart_path[-1]['station'] != full_path[-1]['station']:
            smart_path.append(full_path[-1])

        return smart_path