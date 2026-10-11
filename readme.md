# **Set Covering Problem - Tarea 2 - Optimización**

**Integrantes:** Francisco Carrasco Bugueño 

**RUT:** 21.108.709-9



## **Instrucciones de uso**:


### Requisitos

- Python 3.11.2 (sin librerías externas, solo módulos estándar)


### Archivos necesarios

```
FranciscoCarrasco_SCP.py       # Programa principal
SCP_simple1.txt     # Instancia pequeña de prueba
SCP_simple2.txt     # Instancia pequeña de prueba
01_facil.txt        # Instancia fácil
02_medio.txt        # Instancia media
03_dificil.txt      # Instancia difícil
```

Los archivos de instancia deben estar en la **misma carpeta** que el programa.



### Ejecución

```bash
python3 FranciscoCarrasco_SCP.py
```

El programa ejecuta automáticamente todos los archivos definidos en la lista `archivos` al final del código. Por defecto corre sobre `SCP_simple1.txt`, `SCP_simple2.txt`, `01_facil.txt`, `02_medio.txt.txt` y `03_dificil.txt`.

---
### Cambiar las instancias a ejecutar

Para cambiar qué instancias se resuelven, edita las dos listas `archivos` al final del archivo. La primera controla la fuerza bruta y la segunda el GA:

```python
archivos = [archivos que quieras ejecutar]
```

### Formato de las instancias

```
n m
c1 c2 c3 ... cm
k
j1 j2 ... jk
k
j1 j2 ...
...
```

- `n`: número de elementos a cubrir
- `m`: número de subconjuntos disponibles
- `c1 ... cm`: costo de cada subconjunto (pueden ocupar varias líneas)
- Luego para cada uno de los `n` elementos: cuántos subconjuntos lo contienen y cuáles son (también pueden ocupar varias líneas)

---

## Parámetros del GA

Se pueden ajustar al inicio de la sección del GA en el código:

| Parámetro        | Variable           | Valor por defecto | Descripción                                      |
|------------------|--------------------|-------------------|--------------------------------------------------|
| Tamaño población | `tamanoPoblacion`    | 50                | Cantidad de individuos base y cantidad de hijos generados por ciclo.             |
| Generaciones     | `cantGeneraciones` | 20               | Número de iteraciones del GA                     |
| Tamaño torneo    | `tamanoTorneo`       | 10                 | Cantidad de candidatos evaluados aleatoriamente para seleccionar un padre. selección           |               |
| Ejecuciones      | `numEjecuciones`  | 10                | Veces que se repite el GA para obtener estadísticas |

---
## Salida del programa
```
Ejecución 1: costo = 165, tiempo = 1.2672 seg
Ejecución 2: costo = 170, tiempo = 0.9549 seg
...
========== RESULTADOS GA ==========
Subconjuntos seleccionados: [6,9,11,...]
Mejor costo encontrado: 154
Valores obtenidos: [165, 170, 162, 161, 162, 154, 169, 164, 171, 161]
Media: 163.9000
Desviación estándar: 5.1305
Tiempo total: 10.9960 segundos
==============FIN==================
```

## Arquitectura y Optimizaciones del Algoritmo Genético
Esta versión implementa varias mejoras arquitectónicas para resolver instancias complejas en el menor tiempo posible:
- **Mutación Dinámica**: La probabilidad de mutación no es un parámetro estático, sino que se calcula dinámicamente como $\frac{1}{m}$ (donde $m$ es el número de subconjuntos). Esto asegura un promedio óptimo de alteraciones sin destruir el material genético útil
- **Supervivencia Mixta $(\mu + \lambda) $**: En cada generación se genera una población completa de hijos. Posteriormente, padres e hijos se agrupan y ordenan por costo, sobreviviendo únicamente los individuos más aptos para la siguiente iteración. Esto garantiza un fuerte elitismo y rápida convergencia.
- **Operaciones de Conjuntos Nativas (`Sets`)**: La estructura de datos de las coberturas y la función `reparar` fueron optimizadas para utilizar operaciones a nivel de memoria nativa de Python. Esto elimina el recálculo y reduce drásticamente el tiempo de ejecución en instancias grandes.
