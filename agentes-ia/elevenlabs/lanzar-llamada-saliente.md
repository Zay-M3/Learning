# Lanzar Llamada Saliente

Ya tenemos todo preparado: el agente configurado, las tools enganchadas, los overrides habilitados y las variables listas. Ahora toca lo que de verdad importa: hacer que suene el teléfono del cliente.

---

## Usando el SDK de ElevenLabs

Se usa el SDK de ElevenLabs, no un curl pelado, porque el SDK ya se encarga de hablar con Twilio por debajo.

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
```

---

## El método outbound_call

La llamada saliente se lanza con un único método. Aquí es donde se junta todo lo que hemos ido montando hasta ahora:

```python
response = client.conversational_ai.twilio.outbound_call(
    agent_id=ELEVENLABS_AGENT_ID,
    agent_phone_number_id=ELEVENLABS_PHONE_NUMBER_ID,
    to_number="+573137022646",
    conversation_initiation_client_data={
        "dynamic_variables": { ... },
        "metadata": {"order_id": "972"},
        "conversation_config_override": {
            "agent": {
                "prompt": {"prompt": prompt_rendered},
                "first_message": first_message_rendered,
            },
            "conversation": {"max_duration_seconds": 300},
        },
    },
)
```

---

## Parámetros obligatorios

| Parámetro | Descripción |
|---|---|
| `agent_id` | Qué agente habla |
| `agent_phone_number_id` | Desde qué número llamamos (el `phnum_...` importado de Twilio al principio) |
| `to_number` | A quién llamamos. **Tiene que ir en formato internacional E.164** (`+34...`, `+57...`). En el proyecto se valida antes de llamar. |

El cuarto parámetro, `conversation_initiation_client_data`, es la "mochila" de la llamada: todo lo personalizado de ese cliente concreto (las variables, el prompt relleno, el first_message y el límite de duración).

---

## Manejo del teléfono en formato E.164

El número tiene que ir en formato internacional E.164. En el proyecto se valida **antes** de llamar para no gastar una llamada con un número imposible.

```python
# Ejemplo de validación
if not phone.startswith('+'):
    phone = f'+{phone}'
# Se valida que tenga el formato correcto antes de llamar
```

Si el teléfono está mal, ni se contacta a ElevenLabs.

---

## Respuesta y qué extraer

Cuando la llamada se lanza bien, ElevenLabs devuelve una respuesta de la que sacamos dos cosas importantes:

```python
conv_id = getattr(response, "conversation_id", None)  # conv_... → identifica la conversación
call_id = getattr(response, "call_sid", None)         # el SID de la llamada en Twilio
```

El `conversation_id` (formato `conv_...`) es el más importante, porque es el hilo que permite ir a buscar cómo fue la llamada y qué resultado dio. Es lo que devuelve la función: si todo va bien retorna el `conv_id`, y si algo falla devuelve `None` o `False`.

---

## Errores comunes que ya nos tocaron

1. **Cuenta trial de Twilio:** solo puedes llamar a números que tengas verificados en Twilio.
2. **Sin créditos en ElevenLabs:** las llamadas dejan de salir aunque todo el código esté bien.
3. **Overrides deshabilitados:** ElevenLabs rechaza la inicialización y la llamada se cuelga al instante.

Son las tres primeras cosas que conviene revisar si "todo parece correcto" pero el teléfono no suena.

---

## Qué retorna la función

Si todo va bien → retorna el `conv_id`.
Si algo falla (número inválido, sin agente configurado, ElevenLabs rechaza la llamada…) → retorna `None` o `False` para que el resto del sistema sepa que esa llamada no salió.