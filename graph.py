def max_spots_path(graph):
    # Initialize a list to keep track of the longest path found so far
    max_path = []

    # Define a helper function for the backtracking algorithm
    def backtrack(node, visited):
        nonlocal max_path  # Allows access to the max_path variable defined in the outer function
        visited.add(node)  # Mark the current node as visited
        # Update max_path if the current path (visited set) is longer than the longest path found so far
        if len(visited) > len(max_path):
            max_path = list(visited)
        # Explore all unvisited neighbors of the current node
        for neighbor in graph[node]:
            if neighbor not in visited:
                backtrack(neighbor, visited)
        # Backtrack: remove the current node from the visited set before returning to the previous node
        # This allows subsequent explorations to consider this node as a potential part of other paths.
        visited.remove(node)

    # Start the backtracking process from every node in the graph
    for start_node in graph:
        backtrack(start_node, set())  # Use a set for efficient add/remove operations and to avoid revisiting nodes

    return max_path  # Return the longest path found

# Example graph represented as a dictionary
graph = {
    'Spot A': ['Spot B', 'Spot C'],
    'Spot B': ['Spot A', 'Spot C', 'Spot D'],
    'Spot C': ['Spot A', 'Spot B', 'Spot E'],
    'Spot D': ['Spot B'],
    'Spot E': ['Spot C']
}

# Print the path with the maximum number of unique audition spots
print("Path with maximum audition spots:", max_spots_path(graph))