import itertools
import time
import random

#Parámetros globales de algoritmos genéticos
tamanoPoblacion = 1

def extraerInfo(nombreArchivo):
    """
    Esta función lee línea por línea el archivo de instancia de Set Covering Problem y guarda la información
    en variables numericas (número de elementos y subconjuntos), un diccionario de costos y un
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

    #Línea 1: n y m
    primeraLinea = file.readline().strip().split()
    numElementos = int(primeraLinea[0])
    numSubconjuntos = int(primeraLinea[1])

    #Línea 2: costos de cada subconjunto (m valores en una sola línea)
    costosLinea = file.readline().strip().split()
    for i in range(numSubconjuntos):
        costos[i + 1] = int(costosLinea[i])
        cobertura[i + 1] = []

    #Luego, para cada elemento del 1 al n, hay  líneas:
    #Primera: cuántos subconjuntos contienen al elemento j
    #Segunda: cuáles son esos subconjuntos
    for elemento in range(1, numElementos + 1):
        cantSubconjuntos = int(file.readline().strip())
        subconjuntosQueLoContienen = list(map(int, file.readline().strip().split()))
        # Añadimos el elemento j a la cobertura de cada subconjunto que lo contiene
        for sub in subconjuntosQueLoContienen:
            cobertura[sub].append(elemento)

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
    Genera un individuo aleatorio como vector binario de largo numSubconjuntos.
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

ruta = "Instancias/"
archivos = ["SCP_simple1.txt", "SCP_simple2.txt"]
for archivo in archivos:
    nombreArchivo = ruta+archivo
    instancia = extraerInfo(nombreArchivo)
    numElementos, numSubconjuntos, costos, cobertura = instancia

    
    individuo = individuoAleatorio(numSubconjuntos)
    print(f"\nindividuo ->{individuo}")
    print(f"el individuo es válido?: {individuoValido(individuo,numElementos,cobertura)}")
    print(f"costo del individuo: {costoIndividuo(individuo,costos)}")
