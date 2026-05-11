import numpy as np


def check_vertex(vertex, vertices_count):
    if vertex < 0 or vertex >= vertices_count:
        raise ValueError(f"Вершины {vertex} нет в графе")


def outgoing_arcs(graph, representation, vertex):
    """
    Возвращает список дуг, исходящих из вершины vertex.
    Формат результата: [(i, j), ...], где i - откуда, j - куда.

    Поддерживаемые representation:
    - "adjacency_matrix" ("матрица смежности")
    - "incidence_matrix" ("матрица инцидентности")
    - "adjacency_list" ("список смежности")
    - "arc_list" ("список дуг")
    - "ordered_arc_list" ("упорядоченный список дуг")
    """

    rep = representation.lower()

    if rep == "adjacency_matrix":
        matrix = np.array(graph)
        check_vertex(vertex, matrix.shape[0])
        return [(vertex, j) for j in range(matrix.shape[0]) if matrix[j, vertex] == 1]

    if rep == "incidence_matrix":
        matrix = np.array(graph)
        check_vertex(vertex, matrix.shape[0])
        result = []
        for arc_index in range(matrix.shape[1]):
            if matrix[vertex, arc_index] == 1:
                to_vertices = np.where(matrix[:, arc_index] == -1)[0]
                for to_vertex in to_vertices:
                    result.append((vertex, int(to_vertex)))
        return result

    if rep == "adjacency_list":
        if vertex not in graph:
            raise ValueError(f"Вершины {vertex} нет в графе")
        return [(vertex, j) for j in graph[vertex]]

    if rep == "arc_list":
        arcs = np.array(graph)
        vertices = set(arcs[:, 0]) | set(arcs[:, 1])
        if vertex not in vertices:
            raise ValueError(f"Вершины {vertex} нет в графе")
        return [(int(i), int(j)) for i, j in arcs if i == vertex]

    if rep == "ordered_arc_list":
        pointers, to_vertices = graph
        check_vertex(vertex, len(pointers) - 1)
        start = pointers[vertex]
        end = pointers[vertex + 1]
        return [(vertex, int(to_vertices[i])) for i in range(start, end)]

    raise ValueError("Неизвестное представление графа")


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
    3, 4,        # из 0
    0,           # из 1
    0, 1, 3, 4,  # из 2
    1, 4         # из 3
])

if __name__ == "__main__":
    vertex = 0

    print("Вершина:", vertex)

    print("Матрица смежности:",
          outgoing_arcs(adjacency_matrix, "adjacency_matrix", vertex))

    print("Матрица инцидентности:",
          outgoing_arcs(incidence_matrix, "incidence_matrix", vertex))

    print("Список смежности:",
          outgoing_arcs(adjacency_list, "adjacency_list", vertex))

    print("Список дуг:",
          outgoing_arcs(arc_list, "arc_list", vertex))

    print("Упорядоченный список дуг:",
          outgoing_arcs((forward_star_pointers, forward_star_to),
                        "ordered_arc_list", vertex))
