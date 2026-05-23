# Patrones de System Prompt para Agentes

## La pregunta clave: ¿razonar o no razonar?

No es "siempre razona" ni "nunca razones" — depende del **tipo de tarea**:

- **Tareas estructuradas** (una respuesta correcta) → No razones, solo ejecuta
- **Tareas abiertas** (múltiples opciones válidas) → Sí razona, pero con datos

---

## Patrón 1 — FAQ (No razonar)

Para intenciones fijas y frecuentes: consultar estado, cancelar, editar.

**Cuando el usuario pide algo que tiene ruta fija:**
→ No pienses. No razonas. Ejecuta la ruta.

```
[EDITAR PEDIDO]
User dice: "cambiar", "modificar", "editar"
→ Paso 1: Extraer ID del pedido. Si no existe → preguntar.
→ Paso 2: Extraer campo a cambiar. Si no existe → preguntar.
→ Paso 3: Extraer nuevo valor. Si no existe → preguntar.
→ Paso 4: Confirmar → "Vas a cambiar [campo] a [valor] en pedido #[ID]. ¿Confirmas?"
→ Paso 5: Ejecutar tool
→ Paso 6: Reportar resultado
```

**Regla:** Si falta un parámetro, pregunta SOLO ese parámetro. Nunca inventes valores.

---

## Patrón 2 — Tool-Calling Estructurado (No razonar)

Para llamar APIs con parámetros específicos.

**El system prompt le dice exactamente:**
- Qué tool llamar
- Con qué parámetros
- En qué orden

```
[CONSULTAR ESTADO]
→ Solo ejecutar: tool.get_order_status(id)
→ Devolver el estado tal cual. No inventar fechas.
→ Si no existe el pedido → "No encontré ese pedido. ¿El ID es correcto?"
```

**Regla:** El agente no decide qué campos pasar — el prompt le dice exactamente qué campos. Si el modelo inventa parámetros, está mal configurado.

---

## Patrón 3 — Flowchart / Árbol de decisiones (Mínimo razonamiento)

Para flujos condicionales con ramas definidas.

```
[CANCELAR PEDIDO]
→ ¿El usuario confirmó?
  → No: "¿Estás seguro de que quieres cancelar?"
  → Sí: Ejecutar tool.cancel_order(id)
→ ¿Hay motivo requerido?
  → No: continue
  → Sí: Extraer motivo de la conversación
→ ¿El pedido ya fue enviado?
  → Sí: "No se puede cancelar — ya fue enviado. ¿Quieres hacer una devolución?"
  → No: continue
```

**Regla:** El agente sigue el árbol, no "decide" qué rama tomar basándose en intuición.

---

## Patrón 4 — RAG / Catálogo (Sí razonar)

Para sugerencias, recomendaciones, comparisons.

**Aquí el razonamiento SÍ aporta:**

```
[SUGERIR PRODUCTOS]
→ Consultar catálogo filtrando por: presupuesto, preferencias, historial
→ Generar 2-3 opciones con precio y descripción breve
→ Si no hay matches → ofrecer alternativa más cercana y explicar por qué
→ Nunca inventar productos fuera del catálogo
```

```
[RECOMENDAR POR HISTORIAL]
→ Consultar últimos 5 pedidos
→ Identificar patrón (mismo producto, misma categoría, mismo precio)
→ Sugerir basado en ese patrón: "Basado en tus compras recientes..."
```

**Regla:** El razonamiento busca en datos reales, no inventa. Si no hay datos, lo dice.

---

## Resumen — Tabla de decisión

| Patrón | Cuándo usar | ¿Razonar? |
|---|---|---|
| FAQ | Intenciones fijas (cancelar, consultar, editar) | No |
| Tool-calling | Llamar APIs con parámetros exactos | No |
| Flowchart | Flujos condicionales (sí/no → siguiente paso) | Mínimo |
| RAG/Catálogo | Sugerencias, recomendaciones, comparar opciones | Sí — busca y razona |
| Generativo | Redactar mensajes, explicar decisiones | Sí — pero con límites claros |

---

## Estructura del system prompt por tipo de agente

```
## Flujos estructurados (NO razonar — solo ejecutar)
[EDITAR...] → pasos rígidos
[CONSULTAR...] → solo tool

## Consultas abiertas (SÍ razonar)
[SUGERIR...] → buscar en catálogo, generar opciones
[RECOMENDAR...] → usar historial, explicar lógica
```

**La clave:** ambos modos conviven en el mismo system prompt, pero separados por contexto claro. Cada intent tiene su zona.

---

*Contenido: Mayo 2026 — Patrones discutidos con David para agentes WhatsApp*