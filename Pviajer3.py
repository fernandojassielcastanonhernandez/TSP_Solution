import random                       //importacion de librerias
import matplotlib.pyplot as plt

def calcular_distancia(ciudad1, ciudad2):                                           //
    return ((ciudad1[0] - ciudad2[0])**2 + (ciudad1[1] - ciudad2[1])**2)**0.5

def generar_matriz_distancias(ciudades):
    num_ciudades = len(ciudades)
    distancias = [[0] * num_ciudades for _ in range(num_ciudades)]
    
    for i in range(num_ciudades):
        for j in range(i+1, num_ciudades):
            distancia = calcular_distancia(ciudades[i], ciudades[j])
            distancias[i][j] = distancia
            distancias[j][i] = distancia

    return distancias

def evaluar_ruta(ruta, distancias):
    longitud = 0
    for i in range(len(ruta) - 1):
        longitud += distancias[ruta[i]][ruta[i + 1]]
    longitud += distancias[ruta[-1]][ruta[0]]
    return longitud

def inicializar_poblacion(num_ciudades, tamano_poblacion):
    poblacion = []
    for _ in range(tamano_poblacion):
        ruta = list(range(num_ciudades))
        random.shuffle(ruta)
        poblacion.append(ruta)
    return poblacion

def seleccionar_padres(poblacion, distancias):
    padres = []
    for _ in range(len(poblacion)):
        torneo = random.sample(poblacion, 3)
        mejor_ruta = min(torneo, key=lambda x: evaluar_ruta(x, distancias))
        padres.append(mejor_ruta)
    return padres

def cruzar(padres):
    hijos = []
    for i in range(0, len(padres), 2):
        punto_cruce = random.randint(0, len(padres[i]) - 1)
        hijo1 = padres[i][:punto_cruce] + [x for x in padres[i + 1] if x not in padres[i][:punto_cruce]]
        hijo2 = padres[i + 1][:punto_cruce] + [x for x in padres[i] if x not in padres[i + 1][:punto_cruce]]
        hijos.extend([hijo1, hijo2])
    return hijos

def mutar(hijos):
    for i in range(len(hijos)):
        if random.random() < tasa_mutacion:
            punto_mutacion = random.sample(range(num_ciudades), 2)
            hijos[i][punto_mutacion[0]], hijos[i][punto_mutacion[1]] = hijos[i][punto_mutacion[1]], hijos[i][punto_mutacion[0]]
    return hijos

def dibujar_ruta(ruta, ciudades):
    x = [ciudades[i][0] for i in ruta]
    y = [ciudades[i][1] for i in ruta]
    x.append(x[0])  # Volver al punto de inicio
    y.append(y[0])
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.scatter(x, y, marker='o', linestyle='-', color='r')
    plt.title("Mejor Ruta")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.show()

def algoritmo_genetico(num_ciudades, tamano_poblacion, num_generaciones, tasa_mutacion):
    ciudades = [(1, 1), (1, 15), (1, 15), (20, 3), (8, 12), (18, 20), (20, 20),(10, 15), (25, 15), (18, 15)]
    distancias = generar_matriz_distancias(ciudades)

    poblacion = inicializar_poblacion(num_ciudades, tamano_poblacion)

    for generacion in range(num_generaciones):
        padres = seleccionar_padres(poblacion, distancias)
        hijos = cruzar(padres)
        hijos_mutados = mutar(hijos)
        poblacion = hijos_mutados

        mejor_ruta = min(poblacion, key=lambda x: evaluar_ruta(x, distancias))
        mejor_longitud = evaluar_ruta(mejor_ruta, distancias)

        print(f"Generación {generacion + 1}: Mejor longitud de ruta = {mejor_longitud}, Mejor ruta = {mejor_ruta}")

    dibujar_ruta(mejor_ruta, ciudades)

# Parámetros
num_ciudades = 10
tamano_poblacion = 10
num_generaciones = 60
tasa_mutacion = 0.3

# Ejecutar el algoritmo genético
algoritmo_genetico(num_ciudades, tamano_poblacion, num_generaciones, tasa_mutacion)
