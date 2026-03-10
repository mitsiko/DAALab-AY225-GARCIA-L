import heapq

# ==========================
# HARD CODED DATASET
# ==========================

edges = [
    (1,2,10,15,1.2),
    (1,6,10,15,1.2),
    (2,1,10,15,1.2),
    (2,3,12,25,1.5),
    (2,6,10,15,1.2),
    (2,5,12,25,1.5),
    (3,2,12,25,1.5),
    (3,4,12,25,1.5),
    (3,5,12,25,1.5),
    (3,6,10,25,1.3),
    (4,3,12,25,1.5),
    (4,5,14,25,1.2),
    (5,2,12,25,1.5),
    (5,3,12,25,1.5),
    (5,4,14,25,1.2),
    (5,6,10,25,1.5),
    (6,1,10,15,1.2),
    (6,2,10,15,1.2),
    (6,3,10,25,1.3),
    (6,5,10,25,1.5)
]

nodes = [1,2,3,4,5,6]

# ==========================
# BUILD GRAPH
# ==========================

graph = {node: [] for node in nodes}

for frm,to,dist,time,fuel in edges:
    graph[frm].append((to,dist,time,fuel))

# ==========================
# DIJKSTRA FUNCTION
# ==========================

def dijkstra(start, parameter_index):
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0
    pq = [(0,start)]
    
    while pq:
        current_distance,current_node = heapq.heappop(pq)
        for neighbor in graph[current_node]:
            next_node = neighbor[0]
            weight = neighbor[parameter_index]
            new_distance = current_distance + weight
            if new_distance < distances[next_node]:
                distances[next_node] = new_distance
                heapq.heappush(pq,(new_distance,next_node))
    
    return distances

# ==========================
# CALCULATE TOTALS
# ==========================

def compute_totals(parameter_index):
    totals = {}
    for node in nodes:
        result = dijkstra(node,parameter_index)
        totals[node] = sum(result.values())
    return totals

# ==========================
# PRINT RESULTS (CLEAN VERSION)
# ==========================

def print_results(title, totals, unit):
    print("\n----------------------------------------")
    print(title)
    print("----------------------------------------\n")
    
    for node in nodes:
        # Use ASCII arrow instead of Unicode
        if "DISTANCE" in title.upper():
            print(f"Node {node} -> Total Distance: {totals[node]:.2f} {unit}")
        elif "TIME" in title.upper():
            print(f"Node {node} -> Total Travel Time: {totals[node]:.2f} {unit}")
        else:
            print(f"Node {node} -> Total Fuel Consumption: {totals[node]:.2f} {unit}")
    
    min_value = min(totals.values())
    lowest_nodes = [str(node) for node,value in totals.items() if value == min_value]
    
    # Join multiple lowest nodes with "and"
    lowest_str = " and ".join(lowest_nodes)
    
    print(f"\nLOWEST TOTAL {title.split(':')[-1].strip()} NODE(S):")
    print(f"Node {lowest_str} ({min_value:.2f} {unit})\n")

# ==========================
# MAIN PROGRAM
# ==========================

distance_totals = compute_totals(1)
time_totals = compute_totals(2)
fuel_totals = compute_totals(3)

# ==========================
# PROGRAM HEADER (Console)
# ==========================


print("\n" + "="*50)
print("SHORTEST PATH ANALYSIS FOR NODES           ")
print("="*50)
print("Description:")
print("  Computes total shortest paths from each node")
print("  to all other nodes based on Distance, Time,")
print("  and Fuel parameters using Dijkstra's algorithm.")



print_results("PARAMETER: DISTANCE", distance_totals, "km")
print_results("PARAMETER: TIME", time_totals, "minutes")
print_results("PARAMETER: FUEL", fuel_totals, "L")