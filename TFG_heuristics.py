import time

def greedy(M, n): # n > 0
    c = [-1] * n # Inicializo el vector coloración
    c[0] = 1
    prohibidos = [False] * n
    for i in range(1, n):
        for j in range(n):
            if M[i][j] == 1 and c[j] != -1:
                prohibidos[c[j] - 1] = True
                
        k = 0
        while k < n and prohibidos[k]:
            k += 1
                
        c[i] = k + 1
        
        prohibidos = [False] * n
    
    return max(c), c
                


def adyacente(M, n, v_recorridos, col, q):  # El vertice v_recorridos es adyacente a algun vertice con el color q
    fila = M[v_recorridos]
    ady = [i for i in range(len(fila)) if fila[i] == 1]
    for v in ady:
        if col[v] == q :
            return False
    return True


def WP(M, n):
    V = []
    
    # Grado de cada vertice
    for v in range(n):
        V.append((v, sum(M[v])))
        
    # Vertices ordenados de mayor a menor grado
    V.sort(key=lambda x: x[1], reverse=True)
    
    col = [-1] * n
    q = 1
    i = 0   # Sigue el orden del grado de mayor a menor

    while i < n :

        v_mayor_grado = V[i][0]     # Vertice de mayor grado en cada iteracion
        col[v_mayor_grado] = q
        for j in range(i + 1, n) :
            v_recorridos = V[j][0]
            if col[v_recorridos] == -1 and adyacente(M, n, v_recorridos, col, q) :                   
                # Condicion: el vertice no tiene asignado color y no es adyacente
                col[v_recorridos] = q

        while i < n and col[V[i][0]] != -1 :  # Preparacion para la siguiente iteracion
            i += 1                  # Hago i el vertice de mayor grado sin color

        q += 1      # Paso al siguiente color
    
    return q - 1, col
        

def RLF(M, n):
    V = []
    for i in range(n):
        V.append(i + 1)
    X = V
    Y = []
    q = 0
    S = []
    i = 0
    while X:
        q += 1
        S_i = []
        
        while X:
           
            if i == 0:
                #print("primer pintado")
                # Elijo k el vertice de mayor grado en X
                grado_maximo = -1 # Si por ejemplo tengo cuatro vertices aislados
                for x in X:
                    grado = 0
                    fila = M[x - 1] # [0,1,1,1,0,0,0,0]
                    for y in X:
                        if fila[y - 1] == 1:
                            grado += 1
                    if grado > grado_maximo:
                        k = x
                        grado_maximo = grado
                #print(k)
                
            else:
                #print("siguiente pintado")
                # Elijo k el vertice en X con mayor numero de aristas a vertices en Y
                aristas_maximo = -1
                for x in X:
                    aristas = 0
                    fila = M[x - 1] # [0,1,1,1,0,0,0,0]
                    for y in Y:
                        if fila[y - 1] == 1:
                            aristas += 1
                    if aristas > aristas_maximo:
                        k = x
                        aristas_maximo = aristas
                #print(k)
                
            i += 1
            S_i.append(k)
            X.remove(k)
            if X:
                fila = M[k - 1]
                aux = [] # Almaceno en aux solamente los adyacentes a k en X
                         # Aunque tambien los añado a Y
                for x in X:
                    if fila[x - 1] == 1:
                        Y.append(x)
                        aux.append(x)
                for y in aux:
                    X.remove(y)
            
        
        S.append(S_i)
        X = Y
        Y = []
        i = 0
        
        
    return q, S


"""
edges = []
with open('queen15_15.txt', 'r') as file:

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
res, clases = WP(adj_matrix, 225)
final = time.time()
t = final - inicio
print(f"{res} colores en {t} tiempo")
"""


