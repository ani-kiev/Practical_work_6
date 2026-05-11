import numpy as np


def _to_arc_list(graph, representation):

    rep = representation.lower()

    if rep == "adjacency_matrix":
        matrix = np.array(graph)
        arcs = []

        for from_vertex in range(matrix.shape[1]):
            for to_vertex in range(matrix.shape[0]):
                if matrix[to_vertex, from_vertex] == 1:
                    arcs.append((from_vertex, to_vertex))

        return np.array(arcs, dtype=int), matrix.shape[0]

    if rep == "incidence_matrix":
        # 1 - выход, -1 - вход
        matrix = np.array(graph)
        arcs = []

        for arc_index in range(matrix.shape[1]):
            from_vertex = np.where(matrix[:, arc_index] == 1)[0]
            to_vertex = np.where(matrix[:, arc_index] == -1)[0]

            if len(from_vertex) != 1 or len(to_vertex) != 1:
                raise ValueError("Некорректная матрица инцидентности")

            arcs.append((int(from_vertex[0]), int(to_vertex[0])))

        return np.array(arcs, dtype=int), matrix.shape[0]

    if rep == "adjacency_list":
        arcs = []

        for from_vertex, neighbours in graph.items():
            for to_vertex in neighbours:
                arcs.append((from_vertex, to_vertex))

        vertices_count = max(graph.keys()) + 1
        return np.array(arcs, dtype=int), vertices_count

    if rep == "arc_list":
        arcs = np.array(graph, dtype=int)
        vertices_count = int(np.max(arcs)) + 1
        return arcs, vertices_count

    if rep == "ordered_arc_list":
        # graph = (pointers, to_vertices)
        pointers, to_vertices = graph
        arcs = []

        for from_vertex in range(len(pointers) - 1):
            start = pointers[from_vertex]
            end = pointers[from_vertex + 1]

            for index in range(start, end):
                arcs.append((from_vertex, int(to_vertices[index])))

        return np.array(arcs, dtype=int), len(pointers) - 1

    raise ValueError("Неизвестное начальное представление графа")


def _from_arc_list(arcs, vertices_count, representation):
    rep = representation.lower()

    if rep == "adjacency_matrix":
        # Инвертированная матрица: строка - куда, столбец - откуда
        matrix = np.zeros((vertices_count, vertices_count), dtype=int)

        for from_vertex, to_vertex in arcs:
            matrix[to_vertex, from_vertex] = 1

        return matrix

    if rep == "incidence_matrix":
        matrix = np.zeros((vertices_count, len(arcs)), dtype=int)

        for arc_index, (from_vertex, to_vertex) in enumerate(arcs):
            matrix[from_vertex, arc_index] = 1
            matrix[to_vertex, arc_index] = -1

        return matrix

    if rep == "adjacency_list":
        adjacency_list = {vertex: [] for vertex in range(vertices_count)}

        for from_vertex, to_vertex in arcs:
            adjacency_list[int(from_vertex)].append(int(to_vertex))

        return adjacency_list

    if rep == "arc_list":
        return np.array(arcs, dtype=int)

    if rep == "ordered_arc_list":
        raise ValueError(
            "Перевод в ordered_arc_list по условию задания не требуется")

    raise ValueError("Неизвестное требуемое представление графа")


def convert_graph(graph, from_representation, to_representation):
    """
    Переводит граф из одного представления в другое.

    Поддерживаемые from_representation:
    - "adjacency_matrix"
    - "incidence_matrix"
    - "adjacency_list"
    - "arc_list"
    - "ordered_arc_list"

    Поддерживаемые to_representation:
    - "adjacency_matrix"
    - "incidence_matrix"
    - "adjacency_list"
    - "arc_list"
    """

    arcs, vertices_count = _to_arc_list(graph, from_representation)
    return _from_arc_list(arcs, vertices_count, to_representation)


# ============================================================
# Пример работы на заданном графе
# ============================================================

adjacency_matrix = np.array([
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 1, 1, 0]
])

incidence_matrix = np.array([
    [-1,  0,  0,  0, -1,  1,  1,  0,  0],
    [1, -1,  0,  0,  0,  0,  0, -1,  0],
    [0,  0,  0,  1,  1,  0,  0,  1,  1],
    [0,  1,  1,  0,  0, -1,  0,  0, -1],
    [0,  0, -1, -1,  0,  0, -1,  0,  0]
])

adjacency_list = {
    0: [3, 4],
    1: [0],
    2: [0, 1, 3, 4],
    3: [1, 4],
    4: []
}

arc_list = np.array([
    [1, 0],
    [3, 1],
    [3, 4],
    [2, 4],
    [2, 0],
    [0, 3],
    [0, 4],
    [2, 1],
    [2, 3]
])

forward_star_pointers = np.array([0, 2, 3, 7, 9, 9])

forward_star_to = np.array([
    3, 4,
    0,
    0, 1, 3, 4,
    1, 4
])

ordered_arc_list = (forward_star_pointers, forward_star_to)

if __name__ == "__main__":
    print("Матрица смежности -> список дуг:")
    print(convert_graph(adjacency_matrix, "adjacency_matrix", "arc_list"))

    print("\nСписок дуг -> матрица инцидентности:")
    print(convert_graph(arc_list, "arc_list", "incidence_matrix"))

    print("\nУпорядоченный список дуг -> список смежности:")
    print(convert_graph(ordered_arc_list, "ordered_arc_list", "adjacency_list"))
