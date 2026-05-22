# Tecnicas de Elicitacion de Requisitos

Como extraer los requisitos reales del cliente — no los que dice que quiere, sino los que necesita.

## El problema fundamental

El cliente dice "quiero un CRM". Pero lo que necesita es no perder clientes por falta de seguimiento. El CRM es la solucion tecnica — el problema real es otro. 

Nuestro trabajo es descubrir el problema real.

---

## Tecnica 1: Los 5 Porques

Preguntas递归 hasta encontrar la causa raiz del requerimiento.

Cliente: "Quiero un sistema de notificaciones"
- Por que? Porque los trabajadores olvidan hacer cosas
- Por que olvidan? Porque no hay un registro de tareas
- Por que no hay registro? Porque todo es en papel o en WhatsApp
- Por que todo es en WhatsApp? Porque es lo mas rapido
- Por que lo mas rapido? Porque el proceso actual es muy engorroso

Conclusion: El problema real no es notificaciones — es que el proceso de registrar tareas es demasiado lento. La solucion podria ser un sistema simple de tareas, no un modulo de notificaciones sofisticado.

---

## Tecnica 2: Observation del trabajo actual

Ir al lugar de trabajo y observar como hacen las cosas actualmente.

Durante la observacion, buscar:
- Donde se producen cuellos de botella?
- Que tareas son repetitivas y consumen tiempo?
- Que informacion tiene que buscar o pedir el trabajador?
- Que pasos podrian eliminarse si hubiera un sistema?

**Regla de oro:** Si puedes automatizar algo que el trabajador hace manualmente 20 veces al dia, eso vale mas que 10 modulos de "reportes ejecutivos".

---

## Tecnica 3: Mapear el flujo actual vs el deseado

Con el cliente, dibuja en Excalidraw el flujo actual:

```
[Cliente llama] → [Recepcionista anota en cuaderno] → [Auxiliar busca en archivos] → [Se demora 2 dias] → [Cliente se va a la competencia]
```

Luego el flujo deseado:

```
[Cliente llama] → [Sistema muestra todo en 3 segundos] → [Se resuelve en la misma llamada]
```

La diferencia entre los dos es donde esta el valor del sistema.

---

## Tecnica 4: El taller de requisitos

Reunir a todas las personas que usan el sistema hoy:
- Quien recibe la informacion?
- Quien la procesa?
- Quien toma decisiones?
- Quien necesita reportes?

Todos ven el negocio desde un angulo diferente. Juntarlos produce una lista de requisitos mucho mas completa.

Cuidado: En estos talleres alguien siempre dice "y si pudieramos hacer X" — eso no es un requisito, es una idea. El requisito es "necesito X para resolver el problema Y".

---

## Tecnica 5: Analisis de incidentes

Preguntar: "Cuenteme la ultima vez que algo salio mal con un cliente. Que paso? Por que paso? Que costo tuvo?"

Los incidentes reales revelan requisitos que las reuniones formales no capturan. La gente cuenta problemas reales, no hipotesis.

---

## Tecnica 6: Prototipar antes de preguntar

Antes de ir a la segunda reunion, construir un prototipo en Excalidraw basado en lo que se entendio en la primera reunion. Mostrarlo y preguntar: "Esto es lo que entendi, es correcto?"

El prototipo funciona como espejo — el cliente ve sus propias palabras reflejadas y puede corregir malentendidos.

---

## Senales de que estas capturando mal los requisitos

1. El cliente dice "es que eso ya lo sabia" — no preguntaste lo suficiente
2. El equipo de desarrollo dice "esto no lo habiamos escuchado antes" — no incluiste a todas las personas
3. Despues de上线, el cliente dice "esta parte no la necesitaba asi" — no validaste prototipos suficientes
4. Los requisitos no funcionales nunca se discutieron — no preguntaste sobre carga, usuarios, seguridad

---

## Siguiente paso

Ver: ejemplos-de-extraccion-requisitos.md para ver tecnicas aplicadas a dominios especificos.