# Recibir el Resultado de la Llamada

Ya hemos hecho la llamada y el agente ha hablado con el cliente. Pero, ¿cómo se entera nuestro CRM de cómo fue? Aquí es donde cerramos el círculo.

Cuando la llamada termina y el agente cuelga (con su tool `end_call`), ElevenLabs nos manda toda la conversación a un endpoint nuestro: el **post-call webhook**.

En el proyecto ese endpoint es: `POST /webhooks/elevenlabs/call-result`

Está en `webhooks.py`. Es un endpoint público (sin login), porque quien lo llama es ElevenLabs, no un usuario. Por eso se protege con una firma.

---

## Qué nos llega

ElevenLabs manda un JSON con este formato:

```json
{
  "type": "post_call_transcription",
  "data": {
    "conversation_id": "conv_xxx",
    "call_duration_secs": 47,
    "metadata": {"order_id": "972"},
    "transcript": [ ... ],
    "tool_results": [ ... ]
  }
}
```

Lo importante es el `type` y el `data`.

---

## Cómo sacamos el resultado

Lo primero que hacemos es buscar el `save_call_result` que el agente guardó durante la llamada. Se busca en varios sitios, porque ElevenLabs lo coloca en uno u otro según el caso (lo hace la función `_extract_save_call_result`):

1. En `data.tool_results`, buscando el que tenga `tool_name == "save_call_result"`
2. Si no, dentro del `transcript`, en los mensajes con `role == "tool"`
3. Si no, en `data.analysis.data_collection_results`

De ahí sacamos el `outcome` (`confirmed`, `reschedule`, `cancel`…), el `summary`, y los datos extra si los hay (nueva fecha, nueva dirección, etc.).

---

## Plan B: deducir el resultado del transcript

¿Y si el agente no llegó a llamar a `save_call_result`? Puede pasar (la llamada se corta, el cliente cuelga de golpe…). Para no perder la información, se tiene un plan B: analizar el propio transcript e intentar deducir el resultado.

Si ni así se saca nada claro, simplemente se registra la llamada y se quita el flag de "pendiente", pero no se inventa un resultado.

---

## De qué pedido era

Una vez se tiene el resultado, se necesita saber a qué pedido pertenece. Se resuelve en este orden:

1. El `order_id` que venga dentro del propio `save_call_result`
2. Si no, el que se mandó en el `metadata` al lanzar la llamada
3. Si no, buscar el pedido por el `conversation_id` (que se guardó cuando se lanzó la llamada)

Si después de todo eso no hay forma de saber el pedido, se devuelve `200` igualmente (para que ElevenLabs no reintente) pero se deja constancia en los logs.

---

## Con el resultado claro, actualizar el CRM

Con el pedido y el resultado ya claros, se monta el objeto `CallResultWebhookPayload` y se le pasa al controlador, que es quien actualiza el pedido en el CRM:

- Cambia estado
- Registra la objeción
- Crea el handoff a un humano si hace falta

---

## Ngrok en local para probar el webhook completo

ElevenLabs vive en internet y tu backend en local vive en `localhost`, así que ElevenLabs no puede alcanzarlo.

Para probar el flujo completo en local se levanta un túnel con ngrok y se configura esa URL como webhook en ElevenLabs:

```bash
ngrok http 8000
# te da: https://a1b2-34-56.ngrok-free.app
# → en ElevenLabs configuras el post-call webhook a:
#   https://a1b2-34-56.ngrok-free.app/webhooks/elevenlabs/call-result
```

Si en local se hace una llamada de prueba y el resultado nunca aparece en el CRM, lo primero que hay que mirar es que la URL de ngrok esté viva y bien puesta en ElevenLabs.

> Esto ya nos mordió una vez: el webhook quedó apuntando a una URL de prueba (`httpbin`) y los resultados de las llamadas nunca llegaban al CRM.