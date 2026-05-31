# Estilos de Arquitectura

> No hay un estilo mejor en abstracto — hay un estilo correcto según el contexto, la organización y el equipo.

---

## Conocer el espacio del problema primero

Antes de elegir un estilo de arquitectura, es importante conocer correctamente el espacio del problema. Esto ayuda a elegir correctamente.

Las restricciones del problema deben estar claras antes de proponer cualquier estilo. Si no se conocen las restricciones, cualquier propuesta es un tiro al aire.

---

## Estilos de arquitectura

### 1. Monolito
Todo vive en un solo proceso. Un solo deploy. La forma más simple de organizar código.

**Cuándo considerarlo:**
- Equipos pequeños
- Problemas bien entendidos y estables
- Necesidad de simplicidad operativa

### 2. Monolito restringido por el problema
Un monolito donde las restricciones del negocio definen las fronteras internas — no por tecnología, sino por el dominio del problema.

**Cuándo considerarlo:**
- Cuando el problema tiene fronteras naturales claras
- Cuando las restricciones del negocio son el factor más importante

### 3. Monolito modular
El mismo deploy, pero con módulos claramente separados que se podrían separar en el futuro. Cada módulo tiene su propia responsabilidad y dependencias dirigidas.

**Cuándo considerarlo:**
- Equipos que van creciendo
- Dominio lo suficientemente maduro para identificar módulos
- Paso intermedio natural antes de migrar a microservicios

### 4. Microservicios
Servicios independientes que se deployan y escalan por separado. Cada uno owning su propio dominio o capacidad.

**Cuándo considerarlo:**
- Equipos con madurez operativa suficiente
- Dominio bien entendido y delimitado
- Necesidad real de escalamiento independiente

> **Nota:** Ir a microservicios sin la madurez del equipo es un error común. La pregunta no es "¿microservicios sí o no?" sino **"¿qué puede operar mi organización hoy sin que se convierta en caos?"**

### 5. Servicios basados en eventos
Los servicios se comunican a través de eventos en lugar de llamadas directas. Un evento se emite y los interesados reaccionan.

**Cuándo considerarlo:**
- Sistemas donde la reacción a发生的事情 es más importante que el flujo directo
- Necesidad de desacoplar productores de consumidores
- Auditoría y trazabilidad de estado

---

## Progresión sugerida

```
Monolito → Monolito restringido → Monolito modular → Microservicios → Eventos
```

Esta progresión sugiere un camino de menor a mayor complejidad, pero **no es rígida**. Todo depende de la estructura que siga la organización.

Factores que determinan cuándo avanzar:
- Madurez del equipo para operar y monitorear
- Claridad del dominio y sus fronteras
- Necesidades reales de escalamiento
- Restricciones de la organización

---

## La decisión correcta

La decisión entre estilos no es técnica en primer lugar — es organizacional. Un estilo que funciona en una empresa establecida puede ser la ruina en una startup, y viceversa.

> No existe el estilo perfecto. Existe el estilo que tu organización puede operar hoy sin convertirse en caos.