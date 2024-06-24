from parent.code.classes.route import Route

def get_total_connections_used(routes: list[Route]) -> set[tuple[str, str, float]]:
    total_connections_used = set()

    for route in routes:
        for connection_list in route.connections_used:
            # Ensure connection is a tuple
            connection = tuple(connection_list)

            # Create the reverse connection tuple
            reverse_connection = (connection[1], connection[0], connection[2])

            # Check if the connection or its reverse has already been used, add if not
            if connection not in total_connections_used and reverse_connection not in total_connections_used:
                total_connections_used.add(connection)

    return total_connections_used