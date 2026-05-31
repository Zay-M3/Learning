# Herramientas de Agente

Hasta ahora nuestro agente sabe hablar y sabe a quién llama, pero no sabe hacer nada con la conversación: ni guardar el resultado, ni colgar. Para eso existen las **tools** (herramientas).

Una tool es una capacidad que le damos al agente para que, en mitad de la llamada, ejecute una acción concreta.

Documentación: [Tools | ElevenLabs](https://elevenlabs.io/docs/conversational-ai/tools)

---

## Tipos de tools

| Tipo | Qué hace | Cuándo usarla |
|---|---|---|
| **server tool** | ElevenLabs hace una petición HTTP a tu URL en tiempo real y espera respuesta | Cuando necesitas consultar datos en tiempo real durante la llamada |
| **client tool** | La acción la "ejecuta el cliente" — el dato queda grabado en la conversación | Cuando solo necesitas guardar/grabar datos sin esperar respuesta |
| **system tool** | Modifica el estado interno de la conversación | Para controlar la propia conversación (colgar, transferir) |

---

## Regla mental

- **client tool** = guarda/envía datos
- **system tool** = controla la propia conversación (colgar, transferir, etc.)

Cada uno vive en un sitio distinto del JSON. Mezclarlos da error.

---

## save_call_result — el client tool

Esta es la herramienta más importante. Cuando el agente termina de hablar con el cliente, llama a `save_call_result` pasándole el resultado: si el pedido quedó confirmado, si hubo objeción, si pidió cambiar la fecha, un resumen, etc.

Está montado como **client tool** con `"expects_response": false`. ¿Por qué? Porque NO necesitamos que ElevenLabs nos llame en mitad de la conversación esperando una respuesta. Lo que hacemos es: dejar que el agente grabe el resultado, y al colgar, ElevenLabs nos manda toda la conversación de golpe por el **post-call webhook**.

El schema de la tool (qué campos puede rellenar el agente) vive en el código, en `SAVE_CALL_RESULT_TOOL_SCHEMA` dentro de `call_provider.py`. Eso garantiza que la tool en ElevenLabs y lo que el backend espera leer estén siempre sincronizados.

### Crear por API

```bash
curl -X POST https://api.elevenlabs.io/v1/convai/tools \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_config": {
      "type": "client",
      "name": "save_call_result",
      "description": "Guarda el resultado de la llamada de confirmación con todos los datos recopilados.",
      "expects_response": false,
      "parameters": {
        "type": "object",
        "required": ["outcome", "summary", "order_id"],
        "properties": {
          "order_id": {
            "type": "string",
            "description": "ID del pedido que se está confirmando."
          },
          "outcome": {
            "type": "string",
            "enum": ["confirmed","reschedule","address_change","cancel","partial_confirm","missing_data","callback_requested","undecided","complaint","no_answer","voicemail","busy","wrong_number","call_failed"],
            "description": "Resultado de la llamada"
          },
          "summary": {
            "type": "string",
            "description": "Resumen breve (máx 200 caracteres)"
          },
          "new_delivery_date": {
            "type": "string",
            "description": "Nueva fecha YYYY-MM-DD. Solo si outcome=reschedule."
          },
          "caller_sentiment": {
            "type": "string",
            "enum": ["positivo","neutral","negativo"],
            "description": "Sentimiento del cliente."
          }
        }
      }
    }
  }'
```

La respuesta nos devuelve un id con formato `tool_...`. Guardarlo, se necesita para adjuntarla al agente.

### Por UI

En el agente, sección **Herramientas → Añadir herramienta → Herramienta cliente**, y rellenas nombre, descripción y los parámetros uno a uno.

La API es más cómoda porque reutiliza el schema del código de un tirón.

---

## end_call — el system tool

Sin esta tool, el agente se quedaría "viva" al acabar y la llamada solo se cortaría por el timeout máximo (5 minutos). `end_call` le permite colgar ella misma en cuanto termina de despedirse.

`end_call` es un **system tool**, así que **NO se crea con POST /tools** ni se mete en `tool_ids`. Se declara dentro del agente, en `conversation_config.agent.prompt.built_in_tools`.

Documentación: [System tools · End call](https://elevenlabs.io/docs/conversational-ai/system-tools)

### Detalle importante que cuesta caro descubrir

Los agentes creados desde el dashboard traen `end_call` activado por defecto, pero los creados/configurados por API **NO**. Si configuras todo por API, tienes que añadir `end_call` a mano o el agente nunca colgará solo.

---

## Cómo lo adjunta el código — El PATCH al agente

Las dos tools se "enganchan" al agente con un `PATCH /v1/convai/agents/{ELEVENLABS_AGENT_ID}`. Fíjate cómo en un mismo bloque conviven los dos sitios distintos:

- `prompt.tool_ids` → aquí va el `tool_...` del client tool (save_call_result)
- `prompt.built_in_tools` → aquí va el system tool (end_call)

```json
{
  "conversation_config": {
    "agent": {
      "prompt": {
        "tool_ids": ["tool_xxxxxxxxxxxxxxxx"],
        "built_in_tools": {
          "end_call": {
            "name": "end_call",
            "description": "Finaliza la llamada cuando la conversación ha terminado.",
            "params": { "system_tool_type": "end_call" }
          }
        }
      }
    }
  }
}
```

### Recuerda

Este PATCH es distinto del PATCH de overrides que vimos antes (`platform_settings.overrides...`). Son dos cosas que el agente necesita:

1. **Overrides habilitados** → para poder inyectarle el prompt/first_message en cada llamada
2. **Tools adjuntadas** → para que sepa guardar el resultado y colgar

---

## Sobre la URL de la tool y ngrok en local

Un client tool (como `save_call_result`) **NO tiene URL**. No apunta a ningún sitio, porque no hace una petición a tu backend: el resultado se queda grabado en la conversación y vuelve después. Así que para `save_call_result` tal como está hoy, no hay nada que apuntar a ngrok.

¿Entonces dónde entra ngrok? En el **post-call webhook**, que es la URL a la que ElevenLabs manda la conversación completa (con los datos de `save_call_result` dentro) cuando la llamada termina.

- **En producción:** `https://tu-dominio.com/webhooks/elevenlabs/call-result`
- **En local:** ElevenLabs no puede llegar a `localhost`, así que se levanta un túnel con `ngrok`:

```bash
ngrok http 8000
# te da algo como: https://a1b2-34-56.ngrok-free.app
# → en ElevenLabs (Settings → Webhooks) se configura:
#   https://a1b2-34-56.ngrok-free.app/webhooks/elevenlabs/call-result
```

> Si en local no ves que se procesen los resultados, lo primero que hay que revisar es que la URL de ngrok esté viva y bien puesta en ElevenLabs.