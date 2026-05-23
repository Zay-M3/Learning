# Background Task + ACK en Agentes WhatsApp (Webhook)

## El problema

WhatsApp exige que el webhook responda con **200 OK en máximo 5 segundos**. Si no respondes, reintenta. Si no respondes después de varios intentos, bloquea tu webhook.

Pero procesar un mensaje con IA (enviar al modelo, esperar respuesta, etc.) puede tardar **10-60 segundos**. Si lo haces dentro del webhook, WhatsApp interpreta timeout = falla y reintenta,，造成 caos.

## La solución: ACK rápido + Background Task

```
WhatsApp → POST /webhook → inmediatamente 200 OK
                          → se dispara Background Task por debajo
                          → mientras, WhatsApp ya está conforme (recibió 200)
```

### Paso a paso

```
1. WhatsApp envía POST a /webhook
2. El handler RECIBE el mensaje, extrae lo que necesita (teléfono, texto, etc.)
3. Inmediatamente responde: return 200 OK, jsonify({"status": "ok"})
4. POR DEBAJO (Background Task): procesar con IA, consultar catálogo, generar respuesta
5. POR DEBAJO: enviar respuesta real al usuario vía WhatsApp API
```

## Implementación en Python (FastAPI)

```python
from fastapi import FastAPI, Request
from fastapi.background import BackgroundTasks
import asyncio

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    
    # Extraer datos rápido
    entry = body.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})
    msg = value.get("messages", [{}])[0]
    
    phone = msg.get("from", "")
    text = msg.get("text", {}).get("body", "")
    
    # ✅ ACK instantáneo — WhatsApp queda conforme
    # NO haces procesamiento de IA aquí
    # Devuelves 200 OK inmediatamente
    
    # ✅ Work por debajo — no bloquea el webhook
    background_tasks.add_task(
        procesar_mensaje,
        phone=phone,
        text=text
    )
    
    return {"status": "ok"}


async def procesar_mensaje(phone: str, text: str):
    """
    Esta función corre POR DEBAJO después del ACK.
    Aquí sí puedes:
    - Enviar a un modelo de IA
    - Consultar base de datos
    - Consultar catálogo
    - Hacer lógica de negocio
    - Enviar respuesta por WhatsApp API
    """
    # 1. Consultar IA (esto puede tardar)
    respuesta = await ia_model.respond(text)
    
    # 2. Enviar respuesta al usuario
    await whatsapp_api.send_message(phone, respuesta)
```

## Mismo patrón en Node.js (Express)

```javascript
app.post('/webhook', async (req, res) => {
    // 1. Extraer datos
    const { phone, text } = extractData(req.body);
    
    // 2. ✅ ACK instantáneo
    res.status(200).json({ status: 'ok' });
    
    // 3. ✅ Work por debajo
    setImmediate(() => procesarMensaje(phone, text));
});

async function procesarMensaje(phone, text) {
    // Procesar con IA
    const respuesta = await iaModel.respond(text);
    
    // Enviar respuesta
    await whatsappApi.sendMessage(phone, respuesta);
}
```

## Por qué NO congelar los workers existentes

Si en vez de background task haces `await ia_model.respond()` directo en el webhook:

```python
# ❌ ESTO BLOQUEA — no hacer
@app.post("/webhook")
async def webhook(request: Request):
    text = await extract_text(request)
    
    # Esto puede tardar 30 segundos
    respuesta = await ia_model.respond(text)  # ⚠️ BLOQUEA
    
    await whatsapp.send(phone, respuesta)
    return {"status": "ok"}  # ⚠️ Llega tarde, WhatsApp ya reintentó
```

Problemas:
1. El worker de FastAPI queda ocupado 30s procesando UN request
2. Si llegan 10 mensajes simultáneos, se acumulan
3. WhatsApp puede reintentar antes de que termine
4. Puedes enviar respuestas duplicadas

## Worker pool + Cola de fondo

```
WhatsApp → ACK 200 → Background Task → [Cola/Queue] → Worker Pool → IA → Respuesta
```

El worker pool procesa por debajo sin bloquear el webhook. Pattern típico:

- **Redis/Bull** para la cola de trabajos
- **Worker separado** que consume de la cola
- **El webhook solo mete el trabajo y responde 200**

```python
@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    job = await extract_job(request.body)
    
    # ✅ ACK instantáneo
    background_tasks.add_task(enqueue_job, job)
    # Usa BullMQ o similar para cola durable
    # El worker procesa cuando pueda
    
    return {"status": "ok"}
```

## Resumen

| Lo que pasa | Tiempo | ¿WhatsApp conforme? |
|---|---|---|
| Recibir mensaje, responder 200 | < 1s | ✅ Sí |
| Procesar con IA | 10-60s | — (ya confirmó) |
| Enviar respuesta real | variable | — |

**La clave:** No mezcles la responsabilidad de "confirmar que recibí" (ACK) con "procesar el mensaje" (Background Task). Son dos jobs distintos en tiempos distintos.

---

*Contenido: Mayo 2026 — Patrón discutido con David para agentes WhatsApp via webhook*