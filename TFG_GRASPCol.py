from random import choice
from itertools import combinations
import time

def get_neighbors(V, E, v):
    neighbors = set()
    for u, w in E:
        if u == v:
            neighbors.add(w)
        elif w == v:
            neighbors.add(u)
    return neighbors

def vertices_grado_maximo(V, E, CSize): 
    degrees = {v: len(get_neighbors(V, E, v)) for v in V}
    sorted_vertices = sorted(degrees.items(), key=lambda item: item[1], reverse=True)
    CL = [v for v, _ in sorted_vertices[:CSize]]
    return CL

def vertices_grado_maximo_en_U(V, U, E, CSize):
    degrees = {v: len(set(get_neighbors(V, E, v)).intersection(U)) for v in V}
    sorted_vertices = sorted(degrees.items(), key=lambda item: item[1], reverse=True)
    CL = [v for v, _ in sorted_vertices[:CSize]]
    return CL

def aristas_resta(V, C, E): # Las aristas (u, v) en E tal que u, v en V - C
    E_star = set()
    for u, v in E:
        if u in V and v in V and u not in C and v not in C:
            E_star.add((u, v))
    return E_star

def f(s, M):
    conflictos = set()
    for conjunto in s:
        for v, w in combinations(conjunto, 2):
            if M[v][w] == 1:
                conflictos.add(v)
                conflictos.add(w)
                
    return conflictos
                


def fase_mejora(V, M, E, i, col):
    s = col
    while len(f(col, M)) == 0:
        # Ordenar col por tamano decreciente de las clases
        col.sort(key=lambda x: len(x), reverse=True)
        k = i - 1
        # Se unen las dos ultimas clases
        V_tilde = [conjunto.copy() for conjunto in s]
        V_tilde[-2] = V_tilde[-2].union(V_tilde[-1])
        # Eliminar el último conjunto
        V_tilde.pop()
        
        s = V_tilde
        # Busqueda local en la solucion 
        s, mejora = LocalSearch(k, s, M)
        
        
        if not mejora:  # En el caso que supera NoImpIter, no consigue una solucion factible con k=i-1 colores
            s = col
            break
        # Si la busqueda local ha mejorado la solucion, se actualiza
        if len(f(s, M)) == 0:
            col = s
    return s
    

    
def LocalSearch(k, s, M, NoImpIter=200):
    NoImprove = 0
    Improvement = False
    s1 = [conjunto.copy() for conjunto in s]
    while len(f(s, M)) > 0 and NoImprove < NoImpIter:
        lista_conflictos = list(f(s, M))
        v_ilegal = choice(lista_conflictos)

        color_actual = -1
        for color, conjunto in enumerate(s):
            if v_ilegal in conjunto:
                color_actual = color + 1
                for elem in conjunto:
                    if elem == v_ilegal:
                        s[color].remove(v_ilegal)
                        break
        mejor_color = color_actual
        mejor_conflictos = len(lista_conflictos)
        for nuevo_color, conjunto in enumerate(s):
            # Probar todas las posibilidades de añadir v_ilegal a otras clases
            if nuevo_color + 1 != color_actual:
                s[nuevo_color].add(v_ilegal)
                nuevos_conflictos = len(f(s, M))
                if nuevos_conflictos < mejor_conflictos:
                    mejor_color = nuevo_color
                    mejor_conflictos = nuevos_conflictos
                    break
                else:
                    s[nuevo_color].remove(v_ilegal)
        if mejor_color == color_actual:
            s[mejor_color - 1].add(v_ilegal)
            NoImprove += 1
        else:
            NoImprove = 0
            Improvement = True
            if len(f(s,M)) == 0:
                s1 = [conjunto.copy() for conjunto in s]

        if NoImprove == NoImpIter:
            Improvement = False
            
    return s1, Improvement

    

def GRASPCol(M, V, E, GIter, CIter, CSize):
    k = len(V)
    col = []
    # Bucle exterior, iteraciones de GRASP
    for it in range(GIter):
        i = 0
        V1 = set(V)
        
        while V1 :
            i += 1
            ecount = float("inf")
            # Empezar fase de construccion
            for j in range(CIter):
                V_temp = set(V1)
                U = set()
                C = set()
                while V_temp:
                    # Construir lista de candidatos
                    if not U:
                        CL = vertices_grado_maximo(V_temp, E, CSize)
                    else:
                        CL = vertices_grado_maximo_en_U(V_temp, U, E, CSize)
                    
                    v = choice(CL)
                    N_v = get_neighbors(V, E, v)
                    C.add(v)
                    U.update(N_v)
                    V_temp.remove(v)
                    V_temp.difference_update(N_v)
                    
                # Determinar las aristas en V1-C
                E1 = aristas_resta(V1, C, E)
                # Actualizar la mejor clase del color
                if len(E1) < ecount:
                    V_i = C
                    ecount = len(E1)
            col.append(V_i)
            V1.difference_update(V_i)
        col = fase_mejora(V, M, E, i, col)
        # Actualizar mejor coloracion
        if len(col) < k:
            resultado = col
            k = len(col)
        col = []
    return resultado


"""
Creo la matriz de adyacencia del grafo a partir del archivo .txt que contiene
la lista de las aristas del grafo. El archivo .txt está extraído de 
https://github.com/Cyril-Grelier/gc_instances , del archivo .edgelist (lista de
aristas).
"""

edges = set()
with open('queen10_10.txt', 'r') as file:
    for line in file:
        u, v = map(int, line.split())
        edges.add((u, v))

# Determinar el tamaño de la matriz de adyacencia
max_node = max(max(pair) for pair in edges)

# Inicializar la matriz de adyacencia con ceros
adj_matrix = [[0] * (max_node + 1) for _ in range(max_node + 1)]

# Rellenar la matriz de adyacencia
for u, v in edges:
    adj_matrix[u][v] = 1
    adj_matrix[v][u] = 1
    
    
# Para comprobar que, efectivamente, es una coloración factible


def es_coloracion_factible(coloracion, matriz_adyacencia):
    # Obtener el número de vértices en la matriz de adyacencia
    num_vertices = len(matriz_adyacencia)
    
    # Iterar sobre cada conjunto en la lista de coloración
    for conjunto in coloracion:
        # Verificar cada par de vértices en el mismo conjunto
        for v1 in conjunto:
            for v2 in conjunto:
                if v1 != v2 and matriz_adyacencia[v1][v2] == 1:
                    # Si dos vértices adyacentes tienen el mismo color, la coloración no es válida
                    return False
    return True

inicio = time.time()
color = GRASPCol(adj_matrix, [i for i in range(100)], edges, 3, 15, 15)
final = time.time()
tiempo = final - inicio
valido = es_coloracion_factible(color, adj_matrix)




