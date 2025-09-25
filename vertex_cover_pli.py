from ortools.linear_solver import pywraplp

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

def vertex_cover_solver(n_value: int):
    try:
        print(f"\nConstruindo o grafo J_{n_value}...")
        vertices_number, edges = create_flower_snark(n_value)
        print(f"Grafo criado com {vertices_number} vértices e {len(edges)} arestas.")

        print(f"Arestas do grafo: {edges}")

        print("-" * 60)
    except ValueError as e:
        print(f"Erro: {e}")
        return

    solver = pywraplp.Solver(
            f'vertex_cover_J{n_value}',
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
    try:
        n_input = input("Digite o índice 'n' para o grafo J_n (ímpar, >= 3): ")
        n = int(n_input)
        vertex_cover_solver(n)
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
