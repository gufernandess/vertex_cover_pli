from ortools.linear_solver import pywraplp

# I begin by forming the “component” of the snark graph.

#  # Then I connect the vertices of the formed component to the successor component.

# I use modulo operations to ensure that vertex indices are within the valid
# range and return to the initial vertex on the last iteration.

def create_goldberg_snark(n: int):
    if not isinstance(n, int) or n < 3 or n % 2 == 0:
        raise ValueError("The index ‘n’ must be an odd integer greater than or equal to 3.")

    vertices_number = 8 * n
    edges = []

    for i in range(n):

        next_i = (i + 1) % n

        # s_i = i
        # t_i = i + n
        # z_i = i + 2*n
        # v_i = i + 3*n
        # w_i = i + 4*n
        # x_i = i + 5*n
        # y_i = i + 6*n
        # u_i = i + 7*n

        edges.append((i, i + n)) # (s_i, t_i)
        edges.append((i + n, next_i)) # (t_i, s_{i+1})

        edges.append((i + 2*n, i + 3*n)) # (z_i, v_i)
        edges.append((i + 4*n, i + 3*n)) # (w_i, v_i)

        edges.append((i + 5*n, i + 6*n)) # (x_i, y_i)
        edges.append((i + 6*n, next_i + 5*n)) # (y_i, x_{i+1})

        edges.append((i + 7*n, next_i + 7*n)) # (u_i, u_{i+1})

        edges.append((i + n, i + 2*n)) # (t_i, z_i)
        edges.append((i, i + 4*n)) # (s_i, w_i)

        edges.append((i + 2*n, i + 5*n)) # (z_i, x_i)
        edges.append((i + 4*n, i + 6*n)) # (w_i, y_i)
        edges.append((i + 3*n, i + 7*n)) # (v_i, u_i)

    return vertices_number, edges

def create_flower_snark(n: int):
    if not isinstance(n, int) or n < 3 or n % 2 == 0:
        raise ValueError("The index ‘n’ must be an odd integer greater than or equal to 3.")

    vertices_number = 4 * n
    edges = []

    # I begin by forming the “component” of the snark graph.

    for i in range(n):
        edges.append((i, i + n))
        edges.append((i, i + 2*n))
        edges.append((i, i + 3*n))


        edges.append((i + n, ((i + 1) % n) + n))

        # In the case of the last iteration, I have to swap the vertex
        # coordinates to ensure that the snark graph is formed correctly.

        if i == n-1:
            edges.append((i + 2*n, ((i + 1) % n) + 3*n))
            edges.append((i + 3*n,((i + 1) % n) + 2*n))

            break

        edges.append((i + 2*n, ((i + 1) % n) + 2*n))
        edges.append((i + 3*n, ((i + 1) % n) + 3*n))

    return vertices_number, edges

def vertex_cover_solver(n_value: int, create_graph_func, graph_name: str):
    try:
        print(f"\nConstructing graph {graph_name}_{n_value}...")
        vertices_number, edges = create_graph_func(n_value)
        print(f"Graph created with {vertices_number} vertices and {len(edges)} edges.")

        print(f"Graph edges: {edges}")

        print("-" * 60)
    except ValueError as e:
        print(f"Error: {e}")
        return

    solver = pywraplp.Solver(
            f'vertex_cover_{graph_name}{n_value}',
            pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
        )

    # For each vertex in the graph, I assign a binary value label that indicates whether the vertex is in the coverage or not.

    x = [solver.IntVar(0, 1, f'x_{i}') for i in range(vertices_number)]

    # I add the restriction that the sum of the values of the vertices of an edge must be greater than or equal to 1, ensuring
    # that at least one of the vertices is selected in the coverage.

    for u, v in edges:
        solver.Add(x[u] + x[v] >= 1)

    # The solver is configured to minimize the objective function, with the goal of finding the combination of vertices that
    # minimizes the size of the coverage while following the imposed constraint.

    solver.Minimize(sum(x[i] for i in range(vertices_number)))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Minimum coverage size per vertex: {int(solver.Objective().Value())}')

        selected_vertices = []
        for i in range(vertices_number):
            if x[i].solution_value() == 1:
                selected_vertices.append(i)

        print(f'Vertices in the roof (one of the possible solutions): {selected_vertices}')
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    print("Select the type of Snark graph to analyze:")
    print("1: Goldberg Snark")
    print("2: Flower Snark")

    choice = input("Type your choice (1 or 2): ")

    graph_func = None
    graph_name = ""

    if choice == '1':
        graph_func = create_goldberg_snark
        graph_name = "Goldberg"
    elif choice == '2':
        graph_func = create_flower_snark
        graph_name = "Flower"
    else:
        print("Invalid choice. Logging out.")

    if graph_func:
        try:
            n_input = input(f"Enter the index ‘n’ for the graph {graph_name}: ")
            n = int(n_input)
            vertex_cover_solver(n, graph_func, graph_name)
        except ValueError:
            print("Invalid input. Please enter an integer.")
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
