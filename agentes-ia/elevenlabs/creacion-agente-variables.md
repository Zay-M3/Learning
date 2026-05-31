# Creación de Agente y Variables de Entorno

---

## Crear el agente

Desde la UI de ElevenLabs, crear un agente en blanco y asignarle un nombre.

Las primeras configuraciones de entrada son importantes tenerlas en cuenta.

---

## Variables de entorno necesarias

### ELEVENLABS_AGENT_ID

Se encuentra directamente entrando al agente, arriba a la derecha en los puntos (menú de opciones). Ahí se encuentra el `agent_id`.

### ELEVENLABS_API_KEY

Nos vamos al menú de la izquierda, abajo del todo en **Desarrollo**. En el menú que aparece, la segunda opción es **Claves de API**. Creamos una clave ahí.

### Permisos requeridos para el agente

- De texto a voz
- De voz a voz
- De voz a texto
- Aislamiento de audio
- ElevenAgents
- Historial
- Modelos
- Webhooks

### ELEVENLABS_PHONE_NUMBER_ID

Se consigue en la sección de números de teléfono.

---

## Importar número desde Twilio

Importante ya tener un número y su SID con el auth token desde Twilio activos.

1. Agregamos la etiqueta y añadimos el número
2. Arriba se puede hacer pruebas
3. Dentro del número añadido, debajo aparece un código que empieza con `phnum_` — ese es el `ELEVENLABS_PHONE_NUMBER_ID`

---

## Configurar variables en .env

```env
ELEVENLABS_AGENT_ID=tu_agent_id
ELEVENLABS_API_KEY=tu_api_key
ELEVENLABS_PHONE_NUMBER_ID=phnum_xxxxx
```

---

> A este punto nuestro agente de voz será un modelo vacío que habla por hablar — sin configuración de prompt ni herramientas todavía.