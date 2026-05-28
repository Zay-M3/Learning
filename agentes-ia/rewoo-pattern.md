# ReWOO — Reason Without Observation

**Paper:** [ReWOO: Decoupling Reasoning from Observations](https://arxiv.org/abs/2305.18323)

## Concepto

ReWOO = **Planificador → Trabajador → Solucionador**

A diferencia de ReAct (piensa → actúa → observa → piensa en loop), ReWOO separa el razonamiento en dos fases: planificas todas las llamadas de una vez, ejecutas en batch, y solo al final razonas sobre los resultados.

**Analogía:**
- ReAct = ir a un mercado sin lista, decides qué comprar en cada pasillo al ver los productos
- ReWOO = hacer la lista en casa, ir al mercado, comprar todo rápido, y solo al salir decides qué cocinar

---

## Arquitectura de 3 Agentes

### 1. Planificador (Planner)

**Rol:** Estructura el plan de ejecución.

**Recibe:**
- La pregunta/objective del usuario
- Lista de herramientas disponibles

**Hace:**
- Divide el problema en subtareas pequeñas y ordenadas
- Define el roadmap: qué hacer primero, segundo, tercero
- Le dice al trabajador qué camino seguir y en qué orden

**Output:**
```markdown
Plan de Ejecución:
1. [Paso 1] → herramienta_a() → extraer dato X
2. [Paso 2] → herramienta_b(X) → usar X para obtener Y
3. [Paso 3] → herramienta_c(Y) → generar resultado Z
```

### 2. Trabajador (Worker)

**Rol:** Ejecuta el plan propuesto por el planificador.

**Recibe:**
- El plan estructurado (roadmap de pasos)
- Las herramientas disponibles

**Hace:**
- Sigue el plan en orden, sin desviarse
- Ejecuta cada herramienta del roadmap
- Almacena TODOS los resultados en un "bag" de evidencia
- No razonar — solo ejecutar y guardar

**Output:**
```markdown
Resultados de Ejecución:
- Paso 1: herramienta_a() → {resultado_X}
- Paso 2: herramienta_b(X) → {resultado_Y}
- Paso 3: herramienta_c(Y) → {resultado_Z}
```

### 3. Solucionador (Solver)

**Rol:** Genera la respuesta final.

**Recibe:**
- La pregunta original del usuario
- El plan que se ejecutó
- Todos los resultados del trabajador

**Hace:**
- Sintetiza: "esto preguntó el usuario → este plan seguí → estos fueron los resultados → mi conclusión"
- Resume y responde de forma dirigida, orientada a la pregunta

**Output:**
```
Respuesta completa al usuario, fundamentada en los resultados del trabajador.
```

---

## Implementación en Código

```python
def rewoo(query, available_tools):
    # Fase 1: Planificador
    plan = planner(
        query=query,
        tools=available_tools,
        system_prompt="Eres un planificador. Dados X y herramientas Y, genera el mejor plan."
    )
    
    # Fase 2: Trabajador
    results = worker(
        plan=plan,
        tools=available_tools,
        system_prompt="Sigue este plan. Ejecuta cada paso y almacena el resultado. No razones, solo ejecuta."
    )
    
    # Fase 3: Solucionador
    response = solver(
        query=query,
        plan=plan,
        results=results,
        system_prompt="Dado la pregunta, el plan y los resultados, genera una respuesta completa."
    )
    
    return response
```

Cada agente tiene su prompt especializado:
- `planner_prompt`: Genera el plan estructurado
- `worker_prompt`: Ejecuta sin razonar, solo almacena
- `solver_prompt`: Resume y responde con el contexto completo

---

## Cuándo usar ReWOO vs ReAct

| Escenario | Patrón | Razón |
|---|---|---|
| Tarea simple (1-2 herramientas) | ReAct | Overhead de planner no vale la pena |
| Múltiples fuentes de info independientes | ReWOO | Planificas todo → ejecutas en paralelo → razonas al final |
| Exploración iterativa (debugging) | ReAct | Necesitas ver resultado anterior para decidir siguiente paso |
| Resumen multifuente (agregar datos de varias APIs) | ReWOO | El planner ve el panorama completo antes de actuar |
| Tareas donde el costo importa | ReWOO | Menos tokens de reasoning intermediario |

---

## Ejemplo Práctico

**Pregunta:** "Dame un resumen del clima en Cali, mis últimos 3 pedidos y el estado de mi cuenta"

### Planificador:
```
Plan:
1. weather(cli="Cali") → obtener_clima
2. orders.get_last(3) → obtener_pedidos
3. account.status() → obtener_cuenta
```

### Trabajador:
```
Resultados:
1. weather(cli="Cali") → {clima: "Soleado, 28°C"}
2. orders.get_last(3) → {pedidos: [...]}  
3. account.status() → {estado: "Al día, límite $500.000"}
```

### Solucionador:
```
Basado en tu consulta:
- Clima en Cali: Soleado, 28°C
- Tus últimos 3 pedidos están en camino (ver detalles)
- Tu cuenta está al día con límite de $500.000
```

---

## Ventajas de ReWOO

1. **Visión del panorama completo** — El planificador ve todas las herramientas antes de actuar
2. **Menos "me olvidé de algo"** — Planificas todas las llamadas de una vez
3. **Más eficiente en tokens** — No haces N loops de think-act-observe
4. **El trabajador no tiene sesgo** — Ejecuta sin contaminarse con resultados anteriores
5. **Parallelizable** — El planner puede definir tareas independientes que se ejecutan en paralelo

---

## Relación con otros patrones

- **ReAct** = Piensa → Actúa → Observa (loop iterativo)
- **ReWOO** = Planifica → Actúa → Resume (2 fases separadas)
- **Plan+Execute** = Similar a ReWOO pero con feedback loops
- **Tree of Thoughts** = Explora múltiples planes en paralelo

ReWOO es en esencia un Plan+Execute donde el reasoning final (solver) recibe todo el contexto de golpe.

---

*Contenido: Mayo 2026 — Documentado por Capo basado en explicación de David*