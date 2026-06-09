# MapReduce

**Creado:** 9 Jun 2026
**Carpeta:** arquitectura-software/
**Relacionado:** [share-nothing.md](./share-nothing.md), [sharding.md](./sharding.md)

---

## Qué es

MapReduce es un **patrón de procesamiento distribuido** para trabajar con datasets gigantes. Parte el trabajo en dos fases: **Map** (procesar pedazos en paralelo) y **Reduce** (juntar y agregar los resultados).

El nombre viene de las dos funciones que lo componen, más un paso intermedio (Shuffle) que las conecta.

## Las 3 fases

### 1. Map — "cada worker barre su pedazo"

El dataset gigante se reparte entre N workers. **Cada worker procesa solo su pedazo, sin hablar con los demás**. Produce resultados intermedios (pares clave-valor).

### 2. Shuffle — "se juntan las piezas"

Los resultados intermedios del mismo "grupo" (misma clave) se mandan al mismo worker para la fase siguiente. **Este es el único momento donde los workers se comunican.**

### 3. Reduce — "se suma y se devuelve el resultado"

Cada worker recibe todos los valores de su grupo y los **agrega** (suma, promedio, count, max, lo que sea) en un resultado final.

## Ejemplo paso a paso

**Problema:** tengo 12 ventas y quiero el total por país.

```python
ventas = [
    "US,100", "CO,50", "US,200", "MX,30",
    "CO,75", "US,40", "MX,10", "CO,20",
    "US,150", "MX,90", "CO,60", "US,80",
]
```

### 🟦 Sharding: partir en 3 pedazos

```
Worker 0 recibe: ['US,100', 'MX,30', 'MX,10', 'MX,90']
Worker 1 recibe: ['CO,50', 'CO,75', 'CO,20', 'CO,60']
Worker 2 recibe: ['US,200', 'US,40', 'US,150', 'US,80']
```

### 🟩 Map: cada worker procesa su pedazo solo

```
Worker 0 produce: [('US', 100), ('MX', 30), ('MX', 10), ('MX', 90)]
Worker 1 produce: [('CO', 50), ('CO', 75), ('CO', 20), ('CO', 60)]
Worker 2 produce: [('US', 200), ('US', 40), ('US', 150), ('US', 80)]
```

### 🟨 Shuffle: agrupar por país

```
US  →  [100, 200, 40, 150, 80]
CO  →  [50, 75, 20, 60]
MX  →  [30, 10, 90]
```

### 🟥 Reduce: sumar

```
US  →  570
CO  →  205
MX  →  130
```

**Resultado final:** `{'US': 570, 'CO': 205, 'MX': 130}`

## Ejemplo completo en Python

```python
from collections import defaultdict

# ============================================================
# SHARDING — partir el trabajo en pedazos (3 workers)
# ============================================================
def shardear(datos, n_shards=3):
    shards = [[] for _ in range(n_shards)]
    for i, item in enumerate(datos):
        shards[i % n_shards].append(item)
    return shards

# ============================================================
# MAP — cada worker procesa SU pedazo, sin hablar con nadie
# ============================================================
def mapear(pedazo):
    pares = []
    for linea in pedazo:
        pais, monto = linea.split(",")
        pares.append((pais, int(monto)))
    return pares

# ============================================================
# SHUFFLE — junta los pares del mismo país en un solo lugar
# ============================================================
def shuflear(resultados_de_todos_los_workers):
    agrupado = defaultdict(list)
    for lista in resultados_de_todos_los_workers:
        for pais, monto in lista:
            agrupado[pais].append(monto)
    return agrupado

# ============================================================
# REDUCE — suma la lista de montos de cada país
# ============================================================
def reducir(grupo_por_pais):
    totales = {}
    for pais, montos in grupo_por_pais.items():
        totales[pais] = sum(montos)
    return totales

# ============================================================
# PIPELINE COMPLETO
# ============================================================
ventas = [
    "US,100", "CO,50", "US,200", "MX,30",
    "CO,75", "US,40", "MX,10", "CO,20",
    "US,150", "MX,90", "CO,60", "US,80",
]

shards = shardear(ventas, n_shards=3)
map_por_worker = [mapear(s) for s in shards]
agrupado = shuflear(map_por_worker)
totales = reducir(agrupado)

print(totales)  # {'US': 570, 'CO': 205, 'MX': 130}
```

## MapReduce y Share Nothing

La conexión es directa:
- **Durante el Map**, cada worker **no comparte nada** con los otros (cada uno con su pedazo, su CPU, su memoria)
- **El Shuffle es la excepción necesaria** — el único momento donde se pasa data entre workers
- **Durante el Reduce**, vuelve a haber aislamiento — cada worker reduce su grupo

| Concepto | Qué se particiona | Dónde se aplica |
|---|---|---|
| **Sharding** | Una base de datos | Persistencia |
| **MapReduce** | Un dataset / trabajo | Procesamiento batch |
| **Share Nothing** | El estado completo (DB + memoria + CPU) | Arquitectura de software |

Los tres viven en la misma familia: *"cortá todo en pedazos, dale cada pedazo a alguien independiente, y al final juntá las respuestas"*.

## Herramientas reales que usan MapReduce

- **Hadoop MapReduce** — el original, pensado para batch sobre datasets de TB/PB
- **Apache Spark** — MapReduce con esteroides, mucho más rápido (procesa en memoria)
- **MongoDB** — soporta operaciones tipo MapReduce sobre colecciones
- **PostgreSQL / BigQuery** — funciones analíticas que replican el patrón map-reduce

## Ventajas

- **Escala a datasets enormes**: un trabajo que tardaría días secuencial, tarda horas en paralelo
- **Tolerancia a fallos**: si un worker se cae, otro agarra su shard
- **Modelo simple**: pensá como Map + Reduce y resolviste el 80% de los casos batch
- **Aprovecha hardware commodity**: no necesitás una bestia, podés usar 100 máquinas chicas

## Desventajas

- **No sirve para todo**: es para batch, no para real-time
- **Shuffle es caro**: cruzar la red entre workers tiene costo
- **El modelo es restrictivo**: no pensás en "queries", pensás en funciones Map y Reduce
- **Latencia alta**: un job MapReduce típico tarda minutos, no milisegundos

## Cuándo usarlo

✅ **Sí, cuando:**
- Tenés datasets que no entran en una sola máquina
- El trabajo es batch (corré cada noche, cada hora, no en tiempo real)
- Tu problema se puede expresar como Map + Reduce (la mayoría de agregaciones sí)

❌ **No, cuando:**
- Necesitás respuesta en milisegundos (usá una DB normal con índices)
- Tu problema requiere muchas iteraciones (ML training con muchas épocas — Spark es mejor)
- El dataset es chico y entra en memoria (overhead no se justifica)

## Resumen en una línea

> **MapReduce** = patrón para procesar datasets gigantes: Map procesa pedazos en paralelo, Shuffle agrupa por clave, Reduce agrega. Es Share Nothing aplicado al procesamiento de datos.

---

*Ver también: [share-nothing.md](./share-nothing.md) (el principio) y [sharding.md](./sharding.md) (cómo partir la DB que alimenta a MapReduce).*
