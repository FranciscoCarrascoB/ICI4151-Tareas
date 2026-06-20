import itertools
import time
import random

#Parámetros globales de algoritmos genéticos
tamanoPoblacion = 50
cantGeneraciones = 20
tamanoTorneo = 10
numEjecuciones = 10

def extraerInfo(nombreArchivo):
    """
    Esta función lee línea por línea el archivo de instancia de SCP y guarda la información
    en variables (número de elementos y subconjuntos), un diccionario de costos y un 
    diccionario de coberturas (qué elementos cubre cada subconjunto).
 
    Formato del archivo:
    - Línea 1: n m (n = número de elementos, m = número de subconjuntos)
    - Línea 2: costos de cada subconjunto separados por espacio (m valores)
    - Luego, para cada elemento j del 1 al n, DOS líneas:
        * Cuántos subconjuntos contienen al elemento j
        * Qué subconjuntos son esos
    """
 
    #numElementos (n): La cantidad de elementos que deben ser cubiertos (universo)
    numElementos = 0

    #numSubconjuntos (m): La cantidad de subconjuntos disponibles
    numSubconjuntos = 0
  
    #costos: El costo de seleccionar cada subconjunto.
    #Guardado en un diccionario: costos[idSubconjunto] = costo (indexado desde 1)
    costos = {}

    #cobertura: Los elementos que cubre cada subconjunto.
    #Se construye invirtiendo la info del archivo: para cada elemento se sabe en qué
    #subconjuntos está, y se invierte para saber qué elementos cubre cada subconjunto.
    #Guardado en diccionario como: cobertura[idSubconjunto] = [elemento1, elemento2, ...] 
    cobertura = {}
 
    file = open(nombreArchivo, "r")
 
    # Línea 1: n y m
    primeraLinea = file.readline().strip().split()
    numElementos    = int(primeraLinea[0])
    numSubconjuntos = int(primeraLinea[1])
 
    # Costos: los m valores pueden venir repartidos en varias líneas.
    # Se siguen leyendo líneas y acumulando valores hasta tener los m costos.
    valoresCostos = []
    while len(valoresCostos) < numSubconjuntos:
        valoresCostos += file.readline().strip().split()
    for i in range(numSubconjuntos):
        costos[i + 1] = int(valoresCostos[i])
        cobertura[i + 1] = set()
 
    # Cobertura: para cada elemento j del 1 al n:
    # - una línea con cuántos subconjuntos lo contienen
    # - los ids de esos subconjuntos, que también pueden venir en varias líneas
    for j in range(1, numElementos + 1):
        cantSubconjuntos = int(file.readline().strip())
        idsSubconjuntos = []
        while len(idsSubconjuntos) < cantSubconjuntos:
            idsSubconjuntos += file.readline().strip().split()
        for k in range(cantSubconjuntos):
            sub = int(idsSubconjuntos[k])
            cobertura[sub].add(j)
 
    file.close()
 
    instancia = [numElementos, numSubconjuntos, costos, cobertura]
    return instancia
    
def mostrarInstancia(numElementos, numSubconjuntos, costos, cobertura):
    """
    Esta función imprime por pantalla los datos de la instancia de SCP:
    el número de elementos a cubrir, el número de subconjuntos disponibles,
    estadísticas de costos y qué elementos cubre cada subconjunto.
    """
    costoTotal = sum(costos.values())
    costoPromedio = costoTotal / numSubconjuntos

    print("============INSTANCIA=============")
    print(f"Número de elementos a cubrir (n): {numElementos}")
    print(f"Número de subconjuntos disponibles (m): {numSubconjuntos}")
    print(f"Costo promedio de los subconjuntos: {costoPromedio:.2f}")
    print(f"Costo mínimo de un subconjunto: {min(costos.values())}")
    print(f"Costo máximo de un subconjunto: {max(costos.values())}")
    print(f"\nCostos de cada subconjunto: {costos}")
    print(f"\nCobertura de cada subconjunto:")
    for sub in cobertura:
        print(f"  Subconjunto {sub} (costo={costos[sub]}): cubre {len(cobertura[sub])} elementos -> {sorted(cobertura[sub])}")

def solucionValida(solucion, numElementos, cobertura):
    """
    Esta función verifica si una solución es válida, comprobando que los subconjuntos
    seleccionados cubran todos los elementos del universo (del 1 al numElementos).
    solucion: lista de ids de subconjuntos seleccionados
    """
    elementosCubiertos = set()
    for sub in solucion:
        for elemento in cobertura[sub]:
            elementosCubiertos.add(elemento)

    universo = set(range(1, numElementos + 1))

    if universo.issubset(elementosCubiertos):
        return True
    return False
    
def costoSolucion(solucion, costos):
    """
    Esta función calcula el costo total de una solución sumando los costos de cada
    subconjunto seleccionado.
    solucion: lista de ids de subconjuntos seleccionados
    """
    costo = 0
    for sub in solucion:
        costo += costos[sub]
    return costo

def compararSoluciones(solucion1, solucion2, numElementos, costos, cobertura):
    """
    Esta función compara dos soluciones e indica cuál es mejor según validez y costo.
    Una solución válida siempre es mejor que una inválida.
    Entre dos soluciones válidas, es mejor la de menor costo.
    """
    valida1 = solucionValida(solucion1, numElementos, cobertura)
    valida2 = solucionValida(solucion2, numElementos, cobertura)
    costo1 = costoSolucion(solucion1, costos)
    costo2 = costoSolucion(solucion2, costos)

    print(f"\nSolución 1: {solucion1}")
    print(f"  Válida: {valida1} | Costo: {costo1}")
    print(f"Solución 2: {solucion2}")
    print(f"  Válida: {valida2} | Costo: {costo2}")

    if valida1 and not valida2:
        print("-> La Solución 1 es mejor (es válida y la Solución 2 no lo es).")
    elif valida2 and not valida1:
        print("-> La Solución 2 es mejor (es válida y la Solución 1 no lo es).")
    elif not valida1 and not valida2:
        print("-> Ninguna solución es válida.")
    else:
        if costo1 < costo2:
            print(f"-> La Solución 1 es mejor (ambas válidas, costo {costo1} < {costo2}).")
        elif costo2 < costo1:
            print(f"-> La Solución 2 es mejor (ambas válidas, costo {costo2} < {costo1}).")
        else:
            print("-> Ambas soluciones son equivalentes (mismo costo y ambas válidas).")

def individuoAleatorio(numSubconjuntos):
    """
    Genera un individuo aleatorio como vector binario de largo "numSubconjuntos".
    Cada bit indica si el subconjunto está seleccionado (1) o no (0).
    """
    return [random.randint(0, 1) for _ in range(numSubconjuntos)]

def individuoValido(individuo, numElementos, cobertura):
    """
    Verifica si un individuo (vector binario) cubre todos los elementos del universo.
    """
    elementosCubiertos = set()
    for i in range(len(individuo)):
        if individuo[i] == 1:
            for elemento in cobertura[i + 1]:
                elementosCubiertos.add(elemento)
 
    universo = set(range(1, numElementos + 1))
    return universo.issubset(elementosCubiertos)
 
def costoIndividuo(individuo, costos):
    """
    Calcula el costo total de un individuo sumando los costos de los subconjuntos activos.
    """
    costo = 0
    for i in range(len(individuo)):
        if individuo[i] == 1:
            costo += costos[i + 1]
    return costo

def generarPoblacionInicial(numSubconjuntos, numElementos, cobertura):
    """
    Genera una población inicial de individuos válidos.
    Descarta los inválidos y sigue generando hasta tener una cantidad de individuos igual a tamanoPoblacion.
    """
    poblacion = []
    while len(poblacion) < tamanoPoblacion:
        individuo = individuoAleatorio(numSubconjuntos)
        if individuoValido(individuo, numElementos, cobertura):
            poblacion.append(individuo)
    return poblacion
 
def seleccionTorneo(poblacion, costos):
    """
    Selecciona un individuo mediante torneo: elige una cantidad de individuos igual a tamanoTorneo al azar
    y retorna el de menor costo.
    """
    candidatos = random.sample(poblacion, tamanoTorneo)
    ganador = candidatos[0]
    for candidato in candidatos[1:]:
        if costoIndividuo(candidato, costos) < costoIndividuo(ganador, costos):
            ganador = candidato
    return ganador
 
def cruzamiento(padre1, padre2):
    """
    Cruzamiento de 1 punto: elige un punto de corte al azar y combina
    la primera mitad del padre1 con la segunda mitad del padre2.
    """
    punto = random.randint(1, len(padre1) - 1)
    hijo = padre1[:punto] + padre2[punto:]
    return hijo
 
def mutacion(individuo, probMutacion):
    """
    Mutación bit-flip: invierte cada bit del individuo usando 
    la probabilidad dinámica calculada en la función genetico().
    """
    mutado = individuo[:]
    for i in range(len(mutado)):
        if random.random() < probMutacion:
            mutado[i] = 1 - mutado[i]
            
    return mutado

def reparar(individuo, numElementos, cobertura, costos):
    
    """
    Esta función recibe un individuo que puede ser inválido, es decir,
    que no cubre todos los elementos del universo, y lo convierte en uno válido activando
    subconjuntos de forma greedy hasta que todos los elementos queden cubiertos.
    Primero se calcula qué elementos ya están cubiertos por los subconjuntos activos (bits en 1).
    Luego entra en un bucle que se repite mientras haya elementos sin cubrir:
        1. Calcula el conjunto de elementos que aún faltan cubrir (sinCubrir).
        2. Recorre todos los subconjuntos inactivos (bits en 0) y para cada uno cuenta
           cuántos elementos de sinCubrir podría cubrir si se activara.
        3. Elige el subconjunto que cubriría más elementos pendientes (criterio greedy).
           Si hay empate entre dos subconjuntos que cubrirían la misma cantidad,
           se prefiere el de menor costo para no encarecer innecesariamente la solución.
        4. Activa ese subconjunto (pone su bit en 1) y actualiza los elementos cubiertos.
    El bucle termina cuando todos los elementos del universo están cubiertos.
    Requiere que el diccionario 'cobertura' almacene sets en lugar de listas.
    """
    reparado = individuo[:]
    
    # 1. Usamos .update() que es mucho más rápido que un ciclo for anidado
    elementosCubiertos = set()
    for i in range(len(reparado)):
        if reparado[i] == 1:
            elementosCubiertos.update(cobertura[i + 1])

    universo = set(range(1, numElementos + 1))
    
    # 2. Calculamos sinCubrir una sola vez al inicio
    sinCubrir = universo - elementosCubiertos

    # 3. Mientras el set 'sinCubrir' tenga elementos (es más rápido que issubset)
    while sinCubrir:
        mejorIdx = -1
        mejorCubriria = -1
        mejorCosto = float('inf')

        for i in range(len(reparado)):
            if reparado[i] == 0:
                # 4. Magia de optimización: cobertura[i+1] YA ES UN SET. 
                # Calculamos la intersección directamente sin conversiones.
                cubriria = len(sinCubrir.intersection(cobertura[i + 1]))

                # Criterio greedy: cubre más, o cubre igual pero es más barato
                if cubriria > mejorCubriria or (cubriria == mejorCubriria and costos[i + 1] < mejorCosto):
                    mejorCubriria = cubriria
                    mejorIdx = i
                    mejorCosto = costos[i + 1]

        # 5. Activamos el ganador
        reparado[mejorIdx] = 1
        
        # 6. En lugar de recalcular todo, simplemente le restamos a 'sinCubrir' 
        # los elementos que este nuevo subconjunto acaba de aportar.
        sinCubrir -= cobertura[mejorIdx + 1]

    return reparado
 
def genetico(numElementos, numSubconjuntos, costos, cobertura):
    """
    Algoritmo genético para resolver el SCP. En cada generación:
    1. Calcula la probabilidad de mutación en base a la instancia (1/m).
    2. Genera una población completa de hijos (50 hijos).
    3. Aplica supervivencia mixta: junta padres e hijos, los ordena por costo 
       y se queda con los 50 mejores para la siguiente generación.
    """
    tiempoInicio = time.time()
    
    poblacion = generarPoblacionInicial(numSubconjuntos, numElementos, cobertura)
    mejorIndividuo = min(poblacion, key=lambda ind: costoIndividuo(ind, costos))
    mejorCosto = costoIndividuo(mejorIndividuo, costos)

    # 1. Cálculo de mutación dinámico (1 dividido por la cantidad de subconjuntos)
    probMutacion = 1.0 / numSubconjuntos

    for generacion in range(cantGeneraciones):
        
        hijos = []
        
        # 2. Generamos 50 hijos por generación
        for _ in range(tamanoPoblacion):
            padre1 = seleccionTorneo(poblacion, costos)
            padre2 = seleccionTorneo(poblacion, costos)

            hijo = cruzamiento(padre1, padre2)
            # Pasamos la probabilidad como parámetro
            hijo = mutacion(hijo, probMutacion) 
            hijo = reparar(hijo, numElementos, cobertura, costos)
            
            hijos.append(hijo)

        # 3. Supervivencia Mixta (Padres e hijos compiten juntos)
        poblacionMixta = poblacion + hijos
        
        # Ordenamos la población mixta de menor a mayor costo
        poblacionMixta.sort(key=lambda ind: costoIndividuo(ind, costos))
        
        # Sobreviven estrictamente los mejores individuos (tamaño de la población original)
        poblacion = poblacionMixta[:tamanoPoblacion]

        # Actualizamos el mejor global evaluando solo al #1 de la nueva población
        mejorActual = poblacion[0]
        costoActual = costoIndividuo(mejorActual, costos)
        
        if costoActual < mejorCosto:
            mejorCosto = costoActual
            mejorIndividuo = mejorActual[:]

    tiempoFin = time.time()
    return mejorIndividuo, mejorCosto, tiempoFin - tiempoInicio
 
def ejecutarGA(numElementos, numSubconjuntos, costos, cobertura):
    """
    Ejecuta el GA una cantidad de veces igual a numEjecuciones y muestra un resumen con la mejor solución
    global, el costo promedio y la desviación estándar.
    """
    resultados = []
    mejorCostoGlobal = float('inf')
    mejorIndividuoGlobal = []
 
    tiempoTotalInicio = time.time()
 
    for ejecucion in range(1, numEjecuciones + 1):
        mejorIndividuo, mejorCosto, tiempoEjecucion = genetico(numElementos, numSubconjuntos, costos, cobertura)
        resultados.append(mejorCosto)
 
        if mejorCosto < mejorCostoGlobal:
            mejorCostoGlobal = mejorCosto
            mejorIndividuoGlobal = mejorIndividuo[:]
 
        print(f"Ejecución {ejecucion}: costo = {mejorCosto}, tiempo = {tiempoEjecucion:.4f} seg")
 
    tiempoTotal = time.time() - tiempoTotalInicio
 
    media = sum(resultados) / len(resultados)
    varianza = sum((r - media) ** 2 for r in resultados) / (len(resultados) - 1)
    desviacion = varianza ** 0.5
 
    # Convertir el mejor individuo (vector binario) a lista de ids de subconjuntos
    subconjuntosSeleccionados = [i + 1 for i in range(numSubconjuntos) if mejorIndividuoGlobal[i] == 1]
 
    print("\n========== RESULTADOS GA ==========")
    print(f"Subconjuntos seleccionados: {subconjuntosSeleccionados}")
    print(f"Mejor costo encontrado: {mejorCostoGlobal}")
    print(f"Valores obtenidos: {resultados}")
    print(f"Media: {media:.4f}")
    print(f"Desviación estándar: {desviacion:.4f}")
    print(f"Tiempo total: {tiempoTotal:.4f} segundos")
    print("==============FIN==================\n")

ruta = "Instancias/"
archivos = ["01_facil.txt","02_medio.txt","03_dificil.txt"]
for archivo in archivos:
    nombreArchivo = ruta+archivo
    instancia = extraerInfo(nombreArchivo)
    numElementos, numSubconjuntos, costos, cobertura = instancia
 
    print(f"\n{'='*10} GA: {archivo} {'='*10}")
    ejecutarGA(numElementos, numSubconjuntos, costos, cobertura)