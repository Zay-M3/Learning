# Variables Dinámicas

El system prompt está lleno de cosas entre dobles llaves: `{{customer_name}}`, `{{order_id}}`, `{{business_name}}`, `{{delivery_date}}`… Son las **variables dinámicas**, y son las que hacen que cada llamada sea distinta aunque el prompt sea siempre el mismo.

La idea es sencilla: el prompt es una plantilla. No se escribe un prompt nuevo por cada cliente, se escribe uno solo con huecos, y en el momento de lanzar la llamada se rellenan esos huecos con los datos reales del pedido.

Documentación oficial: [Dynamic variables | ElevenLabs](https://elevenlabs.io/docs/conversational-ai/dynamic-variables)

---

## Variables que usamos

| Variable | Descripción |
|---|---|
| `customer_name` | Nombre del cliente al que llamamos |
| `order_id` | Número de pedido que vamos a confirmar |
| `business_name` | Nombre de la empresa/socio (obligatorio — si va vacío no se lanza la llamada) |
| `items_summary` | Los productos del pedido, para que el agente los lea |
| `items_readback` | Los productos del pedido en formato de lectura |
| `purchase_date_phrase` | Frase natural de cuándo compró ("ayer", "el pasado sábado"…) |
| `delivery_date` | Fecha de entrega |
| `total_price` | Importe formateado en euros |

---

## Enviarlas en la llamada

Las variables se envían en cada llamada, dentro del campo `conversation_initiation_client_data`, en su apartado `dynamic_variables`.

```json
"conversation_initiation_client_data": {
  "dynamic_variables": {
    "customer_name": "María López",
    "order_id": "972",
    "business_name": "Muebles en Oferta",
    "items_summary": "Lleva:\n— Primero: Sofá 3 plazas...",
    "items_readback": "Lleva:\n— Primero: Sofá 3 plazas...",
    "purchase_date_phrase": "el pasado sábado",
    "delivery_date": "2026-06-02",
    "total_price": "599 €"
  },
  "metadata": {
    "order_id": "972"
  }
}
```

El `metadata` nos sirve luego para saber de qué pedido vino el resultado.

---

## Las dos formas de usarlo (y por qué lo hacemos así)

En el proyecto se hacen las cosas de dos formas a la vez (y es a propósito):

**1. Se rellena el prompt en el código.** Antes de mandar la llamada, se recorre cada variable y se hace un `replace` de `{{customer_name}}` por su valor real sobre el texto del prompt. El prompt que se manda por el override ya va completo, sin huecos. Esto da control total.

**2. Se envían las dynamic_variables igualmente.** Aunque el prompt ya vaya relleno, se siguen enviando las variables por dos motivos:
- Compatibilidad con prompts antiguos que aún esperaban resolverlas del lado de ElevenLabs
- Para que el `first_message` y cualquier otro sitio que use `{{...}}` también se resuelva

---

## Formato completo de conversation_initiation_client_data

Las variables viajan junto al override del prompt, dentro del mismo `conversation_initiation_client_data`:

```json
"conversation_initiation_client_data": {
  "dynamic_variables": {
    "customer_name": "María López",
    "order_id": "972",
    "business_name": "Muebles en Oferta",
    "items_summary": "Lleva:\n— Primero: Sofá 3 plazas...",
    "items_readback": "Lleva:\n— Primero: Sofá 3 plazas...",
    "purchase_date_phrase": "el pasado sábado",
    "delivery_date": "2026-06-02",
    "total_price": "599 €"
  },
  "metadata": {"order_id": "972"},
  "conversation_config_override": {
    "agent": {
      "prompt": {"prompt": "Eres Sofia, una persona real que trabaja en Muebles en Oferta..."},
      "first_message": "¡Hola! Soy Sofia de Muebles en Oferta, ¿hablo con María López?"
    },
    "conversation": {
      "max_duration_seconds": 300
    }
  }
}
```

---

## Requisito: overrides habilitados

Para que ElevenLabs acepte mandar `conversation_config_override` con el prompt y el `first_message`, el agente tiene que tener los overrides habilitados (eso fue lo que hicimos en el PATCH de `platform_settings.overrides`). Si los overrides están desactivados, ElevenLabs rechaza la inicialización y la llamada se cuelga al instante sin que el agente diga nada.

Por eso van siempre de la mano: primero se habilitan overrides en el agente, y luego en cada llamada se mandan los valores.