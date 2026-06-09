# Sharding

**Creado:** 9 Jun 2026
**Carpeta:** arquitectura-software/
**Relacionado:** [share-nothing.md](./share-nothing.md), [mapreduce.md](./mapreduce.md)

---

## Qué es

Sharding es **partir una base de datos grande en pedazos más chicos** (llamados *shards*) y asignar cada shard a un servidor distinto.

Cada shard:
- Tiene una **fracción de los datos totales**
- Vive en **su propio servidor** con su propia CPU, memoria, disco
- Es una **DB chiquita e independiente**
- No comparte nada con los otros shards

## Ejemplo de la vida real

Imaginá una tabla `ventas` con 1.000 millones de registros. Una sola DB no banca la carga, así que la partís:

```
Shard 1 (servidor 1): ventas de US
Shard 2 (servidor 2): ventas de CO
Shard 3 (servidor 3): ventas de MX
Shard 4 (servidor 4): ventas de AR
```

Tu aplicación sabe, según el país, a qué shard preguntar.

## Sharding vs. particionamiento vertical / horizontal

| Término | Qué se parte | Cómo se accede |
|---|---|---|
| **Particionamiento vertical** | Por **columnas** (atributos) | Una tabla partida en columnas, una DB |
| **Sharding (horizontal)** | Por **filas** (registros) | Una tabla partida en filas, cada shard tiene **las mismas columnas pero menos filas** |

Sharding es **particionamiento horizontal**. Cada shard tiene el mismo schema, pero distintas filas.

## Cómo elegir la shard key

La shard key es el campo que decide a qué shard va cada registro. Tiene que cumplir dos cosas:

1. **Distribución pareja** — si shardás por `pais` y el 90% de los datos son de US, el shard de US va a explotar
2. **Co-localización** — los datos que se consultan juntos deberían caer en el mismo shard, así evitás joins entre shards

**Ejemplos típicos de shard keys:**
- `user_id` (cada usuario y sus datos en un shard)
- `pais` + `fecha` (cada país-mes en un shard)
- `tenant_id` (en sistemas multi-tenant, cada cliente en un shard)

## Sharding y Share Nothing

Sharding es **share nothing aplicado a una base de datos**:
- Cada shard es un componente con su DB, su CPU, su memoria
- No comparten estado entre sí
- El router / proxy que sabe a qué shard preguntar es el único "punto de contacto"

```
[App] ──► [Shard Router] ──► Shard 1 (US)
                          ──► Shard 2 (CO)
                          ──► Shard 3 (MX)
```

## Ventajas

- **Escalabilidad horizontal**: si te quedás sin espacio, metés un shard nuevo y redistribuís
- **Tolerancia a fallos**: si un shard se cae, solo perdés esa fracción de los datos
- **Rendimiento**: cada query choca contra una DB chiquita, no contra una bestia

## Desventajas

- **No hay joins entre shards**: si tu query toca dos shards, tenés que hacerla en la app o denormalizar
- **No hay transacciones distribuidas**: no podés hacer `BEGIN; UPDATE shard1; UPDATE shard2; COMMIT;` atómicamente
- **Elección de shard key es dolorosa cambiarla después**: si te equivocaste, redistribuir es un quilombo
- **Hotspots**: si elegís mal la key, un shard recibe más carga que los otros

## Cuándo usarlo

✅ **Sí, cuando:**
- La DB creció más allá de lo que un servidor aguanta
- Tenés un volumen claro de datos y sabés cómo partirlos
- Podés permitirte consistencia eventual entre shards

❌ **No, cuando:**
- La DB todavía entra cómoda en un servidor
- Hacés muchos joins / transacciones cross-partition
- El equipo no tiene la madurez operativa para mantener varios shards

## Resumen en una línea

> **Sharding** = partir una DB grande en pedazos chicos (shards), cada uno en su servidor, sin compartir nada entre ellos. Es share nothing aplicado a datos.

---

*Ver también: [share-nothing.md](./share-nothing.md) (el principio general) y [mapreduce.md](./mapreduce.md) (cómo procesar esos shards en paralelo).*
