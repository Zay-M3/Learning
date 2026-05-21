# Patrones Fundamentales de Agentes IA

## ReAct (Reasoning + Acting)

El patrón más básico para agentes que necesitan razonar y actuar en loop.

**Flujo:**
1. THOUGHT → El modelo razona sobre qué hacer
2. ACTION → Ejecuta una tool/función
3. OBSERVATION → Recibe el resultado
4. (repite hasta tener respuesta final)

## Plan+Execute

Para tareas complejas que necesitan planificar antes de ejecutar.

## Tree of Thoughts

Explora múltiples ramas de razonamiento en paralelo.

## Reflexión

El agente evalúa sus propias respuestas y se autocorrige.

