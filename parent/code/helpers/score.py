from parent.code.classes.route import Route


# Calculate score from list of routes
def calculate_score(routes: list[Route], map: str):
    """
    Calculate the score for a given solution on a given map.

    Pre: routes is a list of Route objects. Map is set correctly to either
    "Holland" or "Nationaal".
    Post: Returns a score as float.

    Args:
        routes (list[Route]): A list of Route objects representing 
        the routes taken.
        map (str): The name of the map on which the routes are calculated 
        (either "Holland" or "Nationaal").
    """
    # Check map
    if map == "Holland":
        total_connections = 28
    elif map == "Nationaal":
        total_connections = 89
    
    connections_used = set()
    total_minutes = 0
    for route in routes:
        for connection in route.get_connections_used():

            # Create reverse connection 
            reverse = (connection[1], connection[0], connection[2])

            # If reverse not in used, then add
            if reverse not in connections_used:
                connections_used.add(tuple(connection))

        # Add route duration to total time
        total_minutes += route.time
    total_connections_used = len(connections_used)
    fraction = total_connections_used / total_connections
    number_of_routes = len(routes)

    # print(f"p: {fraction}, Min:{total_minutes}, T:{number_of_routes}")

    score = fraction * 10000 - (number_of_routes * 100 + total_minutes) 

    return score
