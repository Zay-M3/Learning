# Override desde el SDK y UI

---

## Get conversation token

Dentro del SDK existe el URL endpoint para crear un access token. Este se puede generar sin problemas, se encuentra en la sección **Get conversation token**.

Documentación: [Get conversation token | ElevenLabs Documentation](https://elevenlabs.io/docs/conversational-ai/api/get-conversation-token)

Este endpoint nos sirve para extraer un token de acceso conversacional, el cual podemos usar como una llave temporal para que desde algún lugar se pueda llamar al agente.

```bash
curl -G https://api.elevenlabs.io/v1/convai/conversation/token \
  -d agent_id=ELEVENLABS_AGENT_ID
```

Esto nos retorna una respuesta JSON con un token.

No lo usaremos por que con la configuración de arriba ya dispones del uso del agente sin problemas con permisos altos. Solo es por si acaso.

---

## Dos formas de asignar system prompt y first_message

Antes de comenzar a hablar con el agente, debemos asignarle un **system prompt** y un **first_message** (mensaje de bienvenida). Existen dos formas de hacerlo:

1. **UI del dashboard** — la más simple
2. **Código (PATCH endpoint)** — desde el backend

---

## UI Dashboard — Habilitar overrides

1. Ir a la configuración del agente
2. Ir a **Seguridad** y abajo del todo encontrar el apartado de **sobreescrituras** (override)
3. Activar la parte de **primer mensaje** y **mensaje del sistema**
4. Si no se activa, ElevenLabs no dejará sobreescribir esto desde el endpoint y dará error

---

## PATCH Update Agent — Desde código

 Endpoint: `PATCH https://api.elevenlabs.io/v1/convai/agents/{ELEVENLABS_AGENT_ID}`

Documentación: [Update agent | ElevenLabs Documentation](https://elevenlabs.io/docs/conversational-ai/api/update-agent)

El `agent_id` es obligatorio, no se puede hacer la llamada sin uno válido.

### Headers requeridos

```json
"xi-api-key": "ELEVENLABS_API_KEY"
"Content-Type": "application/json"
```

### Estructura del body

```json
{
  "conversation_config": {
    "turn": {
      "turn_timeout": 2
    },
    "tts": {
      "model_id": "eleven_turbo_v2",
      "voice_id": "cjVigY5qzO86Huf0OWal",
      "agent_output_audio_format": "pcm_16000",
      "optimize_streaming_latency": "3"
    },
    "conversation": {
      "max_duration_seconds": 600,
      "client_events": [
        "audio",
        "interruption"
      ]
    }
  },
  "platform_settings": {
    "overrides": {
      "conversation_config_override": {
        "agent": {
          "first_message": true,
          "prompt": {"prompt": true}
        }
      }
    }
  }
}
```

### Parámetros importantes

| Parámetro | Descripción |
|---|---|
| `turn.turn_timeout` | Segundos de silencio que espera el agente para responder al cliente |
| `tts.model_id` | Modelo de texto a voz |
| `tts.voice_id` | Voz del agente |
| `tts.optimize_streaming_latency` | Latencia de streaming (0 a 4, en string) |
| `conversation.max_duration_seconds` | Máximo permitido que puede durar la conversación |
| `conversation.client_events` | Eventos que pueden ser enviados por el cliente (`audio`, `interruption`) |
| `platform_settings.overrides` | Permite sobreescribir las reglas dentro de la configuración del agente — necesario para enviar prompt y first_message desde el código |