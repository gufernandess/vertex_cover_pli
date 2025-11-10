from ortools.linear_solver import pywraplp

def create_goldberg_snark(n: int):
    if not isinstance(n, int) or n < 3 or n % 2 == 0:
        raise ValueError("O índice 'n' deve ser um inteiro ímpar maior ou igual a 3.")

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
        raise ValueError("O índice 'n' deve ser um inteiro ímpar maior ou igual a 3.")

    vertices_number = 4 * n # O número de vértices de um grafo snark sempre é 4n.
    edges = []

    for i in range(n):
        # Começo formando o "componente" do grafo snark.
        edges.append((i, i + n))
        edges.append((i, i + 2*n))
        edges.append((i, i + 3*n))

        # Depois ligo os vértices do componente formado ao componente sucessor.

        # Uso operações de módulo para garantir que os índices dos vértices estejam dentro do intervalo válido e retornem ao vértice inicial na última iteração.

        edges.append((i + n, ((i + 1) % n) + n))

        # No caso da última iteração, tenho que trocar as coordenadas dos vértices para garantir que o grafo snark seja formado corretamente.

        if i == n-1:
            edges.append((i + 2*n, ((i + 1) % n) + 3*n))
            edges.append((i + 3*n,((i + 1) % n) + 2*n))

            break

        edges.append((i + 2*n, ((i + 1) % n) + 2*n))
        edges.append((i + 3*n, ((i + 1) % n) + 3*n))

    return vertices_number, edges

def vertex_cover_solver(n_value: int, create_graph_func, graph_name: str):
    try:
        print(f"\nConstruindo o grafo {graph_name}_{n_value}...")
        vertices_number, edges = create_graph_func(n_value)
        print(f"Grafo criado com {vertices_number} vértices e {len(edges)} arestas.")

        print(f"Arestas do grafo: {edges}")

        print("-" * 60)
    except ValueError as e:
        print(f"Erro: {e}")
        return

    solver = pywraplp.Solver(
            f'vertex_cover_{graph_name}{n_value}',
            pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING
        )

    # Para cada vértice do grafo, associo um label de valor binário que indica se o vértice está na cobertura ou não.

    x = [solver.IntVar(0, 1, f'x_{i}') for i in range(vertices_number)]

    # Adiciono a restrição de que a soma dos valores dos vértices de uma aresta deve ser maior ou igual a 1, garantindo que pelo menos um dos vértices seja selecionado na cobertura.

    for u, v in edges:
        solver.Add(x[u] + x[v] >= 1)

    # O solver é configurado para minimizar a função objetivo, com o objetivo de encontrar a combinação de vértices que minimiza o tamanho da cobertura e ao mesmo tempo segue a restrição imposta.

    solver.Minimize(sum(x[i] for i in range(vertices_number)))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f'Tamanho mínimo da cobertura por vértices: {int(solver.Objective().Value())}')

        selected_vertices = []
        for i in range(vertices_number):
            if x[i].solution_value() == 1:
                selected_vertices.append(i)

        print(f'Vértices na cobertura (uma das soluções possíveis): {selected_vertices}')
    else:
        print('O problema não possui uma solução ótima.')


if __name__ == '__main__':
    print("Escolha o tipo de grafo Snark para analisar:")
    print("1: Goldberg Snark")
    print("2: Flower Snark")

    choice = input("Digite sua escolha (1 ou 2): ")

    graph_func = None
    graph_name = ""

    if choice == '1':
        graph_func = create_goldberg_snark
        graph_name = "Goldberg"
    elif choice == '2':
        graph_func = create_flower_snark
        graph_name = "Flower"
    else:
        print("Escolha inválida. Saindo.")

    if graph_func:
        try:
            n_input = input(f"Digite o índice 'n' para o grafo {graph_name} (ímpar, >= 3): ")
            n = int(n_input)
            vertex_cover_solver(n, graph_func, graph_name)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
