# Arquitectura Orientada a Eventos

> Un cliente produce, un servidor consume. El evento solo lleva lo necesario — no el flujo completo.

---

## El concepto central: eventos

Un evento representa **una acción que ya sucedio** y que está esperando a ser procesada por el servidor.

A diferencia de una llamada donde el cliente pide y espera respuesta, en la arquitectura orientada a eventos el cliente **no espera**. Emite el evento y sigue. El procesamiento ocurre después, de forma asíncrona.

---

## Qué lleva un evento

Un evento no es un sistema completo ni un flujo completo. Debe tener lo mínimo necesario para que el consumidor sepa:

- **Qué pasó** — el tipo de evento
- **A quién va dirigido** — el identificador del destinatario
- **Qué dato se necesita para procesarlo** — un ID, una referencia, no todo el payload completo

### Ejemplo: FacturaEmitida

```
Evento: FacturaEmitida
- factura_id: "FAC-123"
- cliente_id: "CLI-456"
```

No lleva toda la factura. Lleva lo mínimo para que el consumidor sepa:
- De qué factura se trata (id)
- A quién notificar (cliente_id)

El consumidor, al recibir el evento, sabe dónde dirigirlo y qué representar. No recibe toda la información de la factura, solo la referencia.

---

## Productores y consumidores

La separación entre productores y consumidores es fundamental:

- **Productor (producer):** genera el evento y lo envía. No sabe quién lo consume
- **Consumidor (consumer):** recibe el evento y lo procesa. No sabe quién lo emitió

No se conocen entre sí. Esto es lo que da el desacoplamiento.

---

## El buffer en medio

Entre el producer y el consumer hay un **broker** (Kafka, RabbitMQ, SQS, etc.). Este hace de muro:

- El producer envía el evento al broker
- El broker lo almacena en cola o topic
- El consumer lo lee cuando puede

Esto permite que el producer siga enviando eventos sin esperar a que el servidor procese cada uno. El servidor consume a su ritmo.

También permite que múltiples consumidores escuchen el mismo evento para distintos propósitos.

---

## Relación con DDD (Diseño Dirigido por el Dominio)

Esta arquitectura se basa mucho en DDD. Hay conceptos clave:

### Contexto delimited

El problema se divide en dominios pequeños y separados. Cada contexto maneja su propia lógica de negocio.

### Eventos como resultado de cambios de estado

Los modelos encapsulan las reglas de negocio. Cuando el modelo cambia de estado, eso genera el evento.

```
Factura.confirmar() → estado cambia a "emitida" → se genera evento FacturaEmitida
```

El evento sale del modelo. El modelo es el que sabe cuándo y por quéemitir algo.

### Un concepto de dominio puede vivir en varios contextos

La `Factura` puede existir en el contexto de Ventas y también en el de Contabilidad:

- En **Ventas**: la factura se emite y se envía
- En **Contabilidad**: la factura se valida fiscalmente y se archiva

El evento `FacturaEmitida` es el mismo en ambos contextos, pero cada uno lo interpreta según sus propias reglas. Esto es clave: **el evento cruza contextos**.

---

## Retos de esta arquitectura

### 1. Flujo de tiempo entre eventos y contexto

Cuando un evento cruza varios contextos, el tiempo de procesamiento puede variar entre ellos. Un contexto puede tener el evento listo antes que otro, creando inconsistencias temporales.

### 2. Eventos entrelazados

¿Qué pasa cuando dos eventos dependen uno del otro en el orden?

Ejemplo: `PagoRecibido` y `EnvioIniciado`

- ¿Qué pasa si `EnvioIniciado` llega antes que `PagoRecibido`?
- ¿Se permite procesar el envío sin pago confirmado?
- ¿Se encola y se espera?

Esto requiere reglas claras de orden y consistencia eventual.

### 3. Consistencia eventual

Como el procesamiento es asíncrono, el sistema no garantiza que el estado se actualice de inmediato. El resultado final llegará, pero puede haber un delay. Esto es difícil para equipos acostumbrados a flujos síncronos donde todo pasa en el momento.

### 4. Dificultad en el equipo técnico

Entender el negocio desde la perspectiva de eventos y contextos es complejo. No es trivial ver "cómo funciona el sistema" cuando todo está desacoplado. Por eso se recomienda partir el problema en 3:

1. Dominio
2. Contexto del evento
3. Reglas de cada contexto

---

## Cuándo considerar esta arquitectura

- Sistemas donde la reacción a algo que pasó es más importante que el flujo directo
- Necesidad de desacoplar productores de consumidores
- Auditoría y trazabilidad de estado (tienes todo el historial de eventos)
- Múltiples sistemas que necesitan reaccionar al mismo发生的事情
- Escalabilidad independiente de productores y consumidores

---

## En resumen

| Concepto | Descripción |
|---|---|
| Evento | Algo que ya pasó, con dato mínimo para procesarse |
| Producer | Genera el evento, no espera respuesta |
| Consumer | Procesa el evento, no sabe quién lo emitió |
| Broker | Buffer en medio que almacena y distribuye eventos |
| Consistencia eventual | El resultado llega, pero no inmediatamente |

> La pregunta no es "¿cuándo llegó?" sino "¿qué debe pasar cuando llegue?"