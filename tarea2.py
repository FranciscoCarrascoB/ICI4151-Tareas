import itertools
import time

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

def fuerzaBruta(numElementos, numSubconjuntos, costos, cobertura):
    """
    Esta función aplica fuerza bruta para resolver el problema SCP, evaluando todos los
    subconjuntos posibles de menor a mayor tamaño para encontrar la solución válida de
    menor costo. Se usa "combinations" de la librería itertools.

    La estrategia recorre combinaciones de tamaño 1, luego 2, etc. Al terminar un tamaño
    que produce al menos una solución válida, se detiene: agregar más subconjuntos a
    cualquier solución válida ya encontrada solo puede aumentar el costo.
    """
    subconjuntos = list(costos.keys())

    mejorCosto = float('inf')
    mejorSolucion = []
    solucionesEvaluadas = 0

    #Iniciar el cronómetro
    tiempoInicio = time.time()

    for tamano in range(1, numSubconjuntos + 1):
        for combinacion in itertools.combinations(subconjuntos, tamano):
            solucionesEvaluadas += 1

            solucionActual = list(combinacion)

            if solucionValida(solucionActual, numElementos, cobertura):
                costoActual = costoSolucion(solucionActual, costos)

                if costoActual < mejorCosto:
                    mejorCosto = costoActual
                    mejorSolucion = solucionActual

        #Poda: si ya encontramos al menos una solución válida con 'tamano' subconjuntos,
        #no tiene sentido seguir buscando con más (solo aumentaría el costo mínimo posible)
        if mejorSolucion:
            break

    #Detener el cronómetro
    tiempoFin = time.time()

    elementosCubiertos = set()
    for sub in mejorSolucion:
        for elem in cobertura[sub]:
            elementosCubiertos.add(elem)

    print("\n========== RESULTADOS ==========")
    print(f"Mejor solución encontrada (subconjuntos seleccionados): {mejorSolucion}")
    print(f"Costo mínimo encontrado: {mejorCosto}")
    print(f"Elementos cubiertos: {sorted(elementosCubiertos)}")
    print(f"Cantidad de soluciones revisadas: {solucionesEvaluadas}")
    print(f"Tiempo de ejecución: {tiempoFin - tiempoInicio} segundos")
    print("==============FIN==================\n")

ruta = "Instancias/"
archivos = ["SCP_simple1.txt", "SCP_simple2.txt"]
for archivo in archivos:
    nombreArchivo = ruta+archivo
    instancia = extraerInfo(nombreArchivo)
    numElementos, numSubconjuntos, costos, cobertura = instancia
    
    mostrarInstancia(numElementos, numSubconjuntos, costos, cobertura)

    fuerzaBruta(numElementos, numSubconjuntos, costos, cobertura)