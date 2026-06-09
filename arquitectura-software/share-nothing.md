# Share Nothing

**Creado:** 9 Jun 2026
**Carpeta:** arquitectura-software/
**Relacionado:** [microservicios.md](./microservicios.md), [mapreduce.md](./mapreduce.md), [sharding.md](./sharding.md)

---

## Qué es

Share Nothing ("no compartas nada") es un **principio** de arquitectura de software. Dice que **cada componente es dueño absoluto de sus recursos** y no comparte estado con nadie más.

Cada componente tiene:
- Su propia base de datos
- Su propia memoria
- Su propia CPU / disco
- Su propia lógica

Los componentes **solo se hablan por mensajes o APIs**. Nunca comparten memoria, ni tablas, ni archivos, ni caches.

## Ejemplo de la vida real

Imaginá un sistema de e-commerce con tres componentes:
- **Pedidos** — su DB con tablas `orders`, `order_items`
- **Pagos** — su DB con `transactions`, `refunds`
- **Envíos** — su DB con `shipments`, `tracking`

**Share Nothing puro:**
- Pedidos no lee la DB de Pagos. Si necesita saber si una orden está pagada, llama a la API de Pagos.
- Pagos no escribe en la DB de Envíos. Si un pago se aprueba, dispara un evento y Envíos lo escucha.
- Si la DB de Pagos se cae, Pedidos y Envíos siguen funcionando.

**Lo que NO es share nothing:**
- Pedidos lee directo de la tabla `transactions` de Pagos ❌
- Pagos y Envíos comparten un Redis central con datos de sesión ❌
- Los tres componentes escriben en una misma DB ❌

## Share Nothing vs. Microservicios

**No son lo mismo.** Share Nothing es un *principio*, microservicios es un *estilo arquitectónico* que **usa** share nothing como uno de sus pilares.

| | Share Nothing | Microservicios |
|---|---|---|
| Qué es | Un principio / patrón | Un estilo de arquitectura |
| Decide | "No comparto estado con nadie" | APIs, service discovery, deployment, comunicación, etc. |
| Dónde aplica | En cualquier sistema | En sistemas distribuidos |

Se puede tener **share nothing en un monolito modular** (cada módulo con su DB propia, deployado junto). Y se pueden tener **microservicios que NO son share nothing** (comparten una DB — antipatrón clásico).

## Share Nothing vs. otros patrones

| Patrón | Qué comparte | Cuándo usarlo |
|---|---|---|
| **Share Nothing** | Nada | Microservicios, sistemas distribuidos, datos masivos |
| **Shared Database** | Una DB central | Legacy, equipos chicos, prototipos rápidos |
| **Shared Memory** | Memoria RAM | Sistemas de alto rendimiento en una sola máquina |

## Ventajas

- **Tolerancia a fallos**: si un componente se cae, los demás siguen
- **Escalabilidad independiente**: podés escalar solo el componente que lo necesita
- **Autonomía de equipos**: cada equipo dueño de su componente, sin peleas por el schema
- **Tecnología heterogénea**: cada componente puede usar la DB y el lenguaje que le sirva

## Desventajas

- **Consistencia eventual**: si necesitás datos de otro componente, los pedís por API (latencia)
- **Complejidad operativa**: más DBs para mantener, monitorear, hacer backup
- **Transacciones distribuidas son un dolor**: ya no podés hacer un `BEGIN; ... COMMIT;` que toque dos DBs
- **Más código boilerplate**: cada componente arma su propia infra (conexión a DB, migraciones, etc.)

## Cuándo aplicarlo

✅ **Sí, cuando:**
- El sistema tiene dominios claros y bien separados
- Los equipos son grandes y necesitan autonomía
- Necesitás escalar componentes independientemente
- Procesás datos masivos (MapReduce, Spark, BigQuery)

❌ **No, cuando:**
- Estás haciendo un MVP o prototipo chico
- El equipo es de 2-3 personas
- Los dominios están muy acoplados por negocio (forzar separación te complica la vida)

## El único punto de contacto: el Shuffle / API

Share Nothing dice "no compartas nada", pero **algo tiene que pasar entre componentes**:
- Una **API** (request/response) cuando necesitás una respuesta inmediata
- Un **evento** (publicación/suscripción) cuando te alcanza con enterarte después
- Un **mensaje en una cola** cuando hay trabajo asíncrono

MapReduce lo llama **Shuffle** y es el único momento donde los workers se hablan.

## Resumen en una línea

> **Share Nothing** = regla general donde cada componente tiene su DB, su memoria, su CPU. Los componentes se comunican solo por mensajes/APIs, nunca comparten estado.

---

*Ver también: [sharding.md](./sharding.md) (cómo partir una DB grande) y [mapreduce.md](./mapreduce.md) (cómo procesar datos en paralelo siguiendo este principio).*
