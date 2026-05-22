# Priorizacion de Requisitos

Como decidir que requisitos hacer primero cuando no puedes hacer todos de una vez.

---

## Por que priorizar

En la vida real siempre hay mas requisitos que tiempo y presupuesto. Priorizar no es opcional — es inevitable. La pregunta es si lo haces con criterio o por intuicion.

Si no priorizas, el equipo hace lo que parece mas urgente o lo que mas le gusta. Eso produce sistemas que funcionan pero que no resuelven los problemas mas importantes primero.

---

## Metodo 1: MoSCoW

El mas usado y facil de explicar al cliente.

| Prioridad | Significado | % tipico del backlog |
|---|---|---|
| **M**ust have | Sin esto el sistema no sirve | 60% |
| **S**hould have | Importante pero no critico | 20% |
| **C**ould have | Nice to have | 15% |
| **W**ont have | Esta vez no se hace | 5% |

**Regla:** Solo el 60% de Must Have entra al proyecto. Si tienes mas del 60% en Must, hay que negociar.

---

## Metodo 2: ROI sederhana (Impacto / Esfuerzo)

Graficar cada requisito en una matriz 2x2:

```
                    Alto Esfuerzo
                         |
         Planificable    |   Sinfonico
    [-------------------+-------------------]
    |                   |                   |
Bajo Impacto            |           Alto Impacto
    |   Descartar        |   Hacedlo ahora
    |                   |
    [-------------------+-------------------]
                         |
                    Bajo Esfuerzo
```

**Cuadrante superior izquierdo (Alto impacto, Bajo esfuerzo):** Empieza por aqui.

---

## Metodo 3: Stack Ranking

Ordena todos los requisitos en una lista unica, del 1 al N, segun prioridad.

La regla: entre dos requisitos, cual entregarias primero? Muevelo hacia arriba o hacia abajo hasta que la lista refleje el orden correcto.

Ventaja: forcing function para decisiones. Si no puedes ordenar A antes que B, es que A no es realmente mas importante.

---

## Priorizacion de tu agente de atencion

Aplicando MoSCoW:

| Prioridad | Requisito | Por que |
|---|---|---|
| **Must** | El agente responde preguntas frecuentes | Si no responde nada util, no vale nada |
| **Must** | Tiempo de respuesta menos de 10 segundos | Si es lento, la gente cuelga |
| **Must** | 10+ consultas simultaneas sin degradar | Si solo aguanta 2, no sirve |
| **Should** | Escalada a humano cuando no puede resolver | Critico pero no bloquea |
| **Should** | Historial de conversaciones | Mejora la experiencia |
| **Could** | Reporte de metricas semanal | Nice to have para el negocio |
| **Could** | Integracion con CRM para ver pedido | Complejo, puede ir despues |
| **Wont** | Videollamada con agente | No aplica para texto |

---

## Senales de mala priorizacion

1. Terminaste el proyecto y el cliente dice "eso que mas nos importaba no esta hecho"
2. Hiciste primero la parte tecnicamente interesante, no la que mas valor da
3. Los requisitos no funcionales nunca se priorizaron
4. No tienes forma de explicar al cliente por que ciertos requisitos no entraron en esta fase

---

## Regla del pulgar

Si tienes que elegir entre dos requisitos y no puedes — implica que son iguales de importantes. Preguntale al cliente directo:

"Si solo pudiera tener uno de estos dos, cual elijo?"

La respuesta siempre es reveladora.

---

## Siguiente paso

Ver: senales-requisitos-invalidos.md para aprender a detectar cuando alguien pide algo que no necesita.