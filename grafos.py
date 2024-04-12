import heapq  # Import the heapq module for priority queue operations
import logging  # Import the logging module to log messages

# Configure logging to write to a file with a specific format including timestamp and message level
logging.basicConfig(filename='audition_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def max_spots_min_distance(graph):
    max_path = []  # Initialize the list to store the path that visits the most spots
    min_distance = float('inf')  # Initialize the minimum distance as infinity for comparison
    start_nodes = list(graph.keys())  # Create a list of start nodes from the graph's keys

    def is_valid_graph():
        # Validate the graph by checking if all neighbors are present in the graph and distances are non-negative
        for node, edges in graph.items():
            for neighbor, distance in edges:
                if neighbor not in graph or distance < 0:
                    return False
        return True

    if not is_valid_graph():
        # Log the error using the error level
        logging.error("Error occurred: Invalid graph structure or negative distances")
        # Raise an error if the graph is invalid
        raise ValueError("Invalid graph structure or negative distances")

    for start_node in start_nodes:
        # Initialize a priority queue with the starting node, distance, path, and visited set
        heap = [(0, start_node, [start_node], set([start_node]))]
        while heap:
            # Pop the node with the smallest distance so far from the heap
            distance, node, path, visited = heapq.heappop(heap)
            if distance > 10:
                # Break the loop if the distance exceeds 10 units
                break
            if len(path) > len(max_path) or (len(path) == len(max_path) and distance < min_distance):
                # Update the max path and minimum distance if a better path is found
                max_path = path
                min_distance = distance
            for neighbor, edge_distance in graph[node]:
                if neighbor not in visited:
                    # Calculate new distance and proceed only if it's within the limit
                    new_distance = distance + edge_distance
                    if new_distance <= 10:  
                        # Add the neighbor to the heap with updated distance, path, and visited set
                        heapq.heappush(heap, (new_distance, neighbor, path + [neighbor], visited | {neighbor}))

    # Log the result using the info level
    logging.info("Path with maximum audition spots and minimum distance (within 10 km): %s", result)

    return max_path  # Return the path that visits the most spots within the distance limit

# Example graph represented as a dictionary
graph = {
    'Spot A': [('Spot B', 5), ('Spot C', 10)],
    'Spot B': [('Spot A', 5), ('Spot C', 3), ('Spot D', 7)],
    'Spot C': [('Spot A', 10), ('Spot B', 3), ('Spot E', 8)],
    'Spot D': [('Spot B', 7)],
    'Spot E': [('Spot C', 8)]
}

try:
    result = max_spots_min_distance(graph)
    print("Path with maximum audition spots and minimum distance (within 10 km):", result)
except ValueError as e:
    print("Error:", e)
