from random import randint, choice
import time

def greedy_mod(M, k): # La coloracion del vertice i (i=1,...,n) es c[i - 1] 
                      # Los colores disponibles son q=1,...,k
    n = len(M)
    c = [-1] * n # Inicializo el vector coloración
    c[0] = 1
    prohibidos = [False] * k  # prohibidos[l] indica si en cada iteracion (vertice i) el color l + 1 esta prohibido o no
    for i in range(1, n):
        for j in range(n):
            if M[i][j] == 1 and c[j] != -1: # Los vertices i, j son adyacentes y j esta ya coloreado
                prohibidos[c[j] - 1] = True
        # En este punto ya se que colores estan prohibidos y cuales no para el vertice i
        # Por eso voy a hacer k el menor indice tal que prohibidos[k] es False
        
        q = 0
        while q < k and prohibidos[q]:
            q += 1
        
        if q < k:
            c[i] = q + 1
        
        else: # q == k
            c[i] = randint(1, k)
        
        
        prohibidos = [False] * k

    # Transformo el resultado en las clases (particion)
    
    particion = {}
    
    for v, color in enumerate(c):
        if color not in particion:
            particion[color] = []
        particion[color].append(v)
    
    return particion, c


# Funcion objetivo
def f(M, c):
    n = len(M)
    aristas = []
    for i in range(n):
        for j in range(i + 1, n):  # Basta con recorrer el triangulo superior de la matriz
            if M[i][j] == 1:
                aristas.append((i, j))
    res = 0
    conflictos = set()  # Usar un conjunto para evitar repetidos
    for (u, v) in aristas:
        if c[u] == c[v]:
            res += 1
            conflictos.add((u, c[u]))
            conflictos.add((v, c[v]))
    return len(list(conflictos)), list(conflictos)  # Convertir el conjunto de conflictos a lista antes de devolver


    



def tabucol(M, k, nr_max_it): 
    n = len(M)
    s, c = greedy_mod(M, k)  # s es la particion
    nr_it = 0
    nr_conflictos, conflictos = f(M, c)
    T = [[0 for _ in range(k)] for _ in range(n)]
    C = [[0 for _ in range(k)] for _ in range(n)]
    for v in range(n):
        for j in range(k):
            C[v][j] = 0 
            for w in s[j + 1]:
                if M[w][v] == 1:
                    C[v][j] += 1

    v1 = -1
    i1 = -1
    j1 = -1
    while nr_conflictos > 0 and nr_it < nr_max_it:
        t = 0.6 * nr_conflictos + randint(0, 9)
        print(f"{nr_it} iteraciones")
        
        # Decido cual es el mejor vecino
        
        mejor_nr_conflictos = float("inf")
        
        for (v, i) in conflictos: # v: vertice ; i: color
            for j in range(1, k + 1):
                if j != i and T[v][j - 1] <= nr_it:

                    
                    new_nr_conflictos = nr_conflictos + C[v][j - 1] - C[v][i - 1]
                    if new_nr_conflictos < mejor_nr_conflictos:
                        mejor_nr_conflictos = new_nr_conflictos
                        v1 = v
                        j1 = j
                        i1 = i
        
        # Si todos los movimientos fueran tabu, elijo v al azar y lo muevo al azar a otra clase
        
        if mejor_nr_conflictos == float("inf"):
            v1, i1 = choice(conflictos)
            aux = list(range(i)) + list(range(i + 1, k + 1))
            j1 = choice(aux)
        
        # Actualizar la matriz C
        
        for u in range(n):
            if M[v1][u] == 1:
                C[u][i1 - 1] -= 1
                C[u][j1 - 1] += 1
        
        # Veamos si en la lista tabu alguna solucion es optima (nr_conflictos = 0)
        
        for v in range(n):
            for i in range(k):
                j = c[v]
                if i + 1 != j and T[v][i] > nr_it:
                    new_nr_conflictos = nr_conflictos + C[v][i] - C[v][j - 1]  # Lo llevo de vuelta a S_i desde S_j
                    if new_nr_conflictos == 0:
                        mejor_nr_conflictos = new_nr_conflictos
                        i1 = j
                        j1 = i + 1
                        v1 = v
                        # Actualizar C
                        for u in range(n):
                            if M[v1][u] == 1:
                                C[u][i1 - 1] -= 1
                                C[u][j1 - 1] += 1
        
        
        # Actualizar lista tabu T
        T[v1][i1 - 1] = nr_it + t
        
        # Actualizar s (particion) y c
        s[i1].remove(v1)
        s[j1].append(v1)
        c[v1] = j1
        
        nr_conflictos, conflictos = f(M, c)
        print(f"vertice {v1} desde {i1} hasta {j1}")
        print(nr_conflictos)
        
        nr_it += 1
        
    return s, c
        




"""
Creo la matriz de adyacencia del grafo a partir del archivo .txt que contiene
la lista de las aristas del grafo. El archivo .txt está extraído de 
https://github.com/Cyril-Grelier/gc_instances , del archivo .edgelist (lista de
aristas).

edges = []
with open('school1.txt', 'r') as file:
    for line in file:
        u, v = map(int, line.split())
        edges.append((u, v))
    
# Determinar el tamaño de la matriz de adyacencia
max_node = max(max(pair) for pair in edges)

# Inicializar la matriz de adyacencia con ceros
adj_matrix = [[0] * (max_node + 1) for _ in range(max_node + 1)]

# Rellenar la matriz de adyacencia
for u, v in edges:
    adj_matrix[u][v] = 1
    adj_matrix[v][u] = 1

inicio = time.time()
clases, coloracion = tabucol(adj_matrix, 14, 100000)
final = time.time()
t = final - inicio
print(f"{max(coloracion)} colores en {t} tiempo")


# Para comprobar que, efectivamente, es una coloración factible


def es_coloracion_valida(M, c):
    # M: Matriz de adyacencia
    # c: Vector de coloración, donde c[i] es el color del vértice i
    n = len(M)
    
    # Verificar cada vértice
    for i in range(n):
        for j in range(n):
            if M[i][j] == 1 and c[i] == c[j]:
                # Si dos vértices adyacentes tienen el mismo color, la coloración no es válida
                return False
    return True

valido = es_coloracion_valida(adj_matrix, coloracion)
"""


