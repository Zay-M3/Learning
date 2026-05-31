# Costos y Lenguaje Común en Arquitectura

> Basado en notas de estudio sobre arquitectura de software — capítulo de costos.

---

## La Gestión Estructural Define los Costos

El arquitecto de software debe tener presentes los costos basándose en aspectos **esenciales** y **desechables** del sistema. Para tener esto claro, se debe conocer la **gestión estructural de la empresa**.

### Tipos de empresa por gestión estructural

| Tipo | Estrategia | Prioridad |
|---|---|---|
| **Exploratoria** | Busca su nicho de mercado | Expandir, aprender, encontrar producto-mercado |
| **Con nicho establecido** | Ya conoce su mercado | Invertir en mejorar y eficiencia |
| **Ahorro primero** | Prioriza reducir costos | Costos antes que nuevas funciones |

> Dependiendo del tipo, los costos significan cosas distintas. No se optimiza igual en una startup que en una empresa de ahorro.

---

## ¿Por Qué Ganamos Dinero?

Con la gestión estructural clara, la siguiente pregunta es:

**¿Por qué el cliente nos elige a nosotros?**

Para responderla, se debe trabajar desde ahí para priorizar los requisitos funcionales y no funcionales.

### Preguntas clave

- **¿Nuestro producto es elegido por qué?**
- ¿Tenemos **ventaja competitiva**?
- ¿**Disponibilidad**? (qué tan disponible está el servicio)
- ¿**Precio**?
- ¿Tenemos alguna **insignia** que el cliente busca, como una **ISO**?

Estas preguntas determinan **qué costos importan** y **qué se optimiza primero**.

---

## Análisis de Trade-offs y Costo de Oportunidad

> **权衡 (zhèng huái)** —权衡 —权衡 en chino significa "sopesar, balancear".

Cada decisión arquitectónica tiene un costo de oportunidad: si hacemos A, no hacemos B.

**Trade-off arquitectónico:**
- Alta disponibilidad → mayor costo de infraestructura
- Alta escalabilidad → mayor complejidad
- Tiempo de entrega rápido → posiblemente menor calidad

El arquitecto debe hacer explícitos estos balances, no ocultarlos.

---

## Lenguaje del Dominio del Negocio

**Muy importante:** siempre trabajar con el idioma del dominio del negocio.

El arquitecto de software debe **crear el lenguaje para que todos entiendan** — tanto el problema como la solución.

Si no se hace esto, se cae en el **efecto Babel** (o problema de la torre):

### El Efecto Babel

> Una organización donde todos buscan el mismo objetivo pero hablan idiomas diferentes → la solución no funciona.

**Responsabilidad del arquitecto:** diseñar y facilitar esta manera de comunicación.

### Matriz de Traducción Técnico → Negocio

Una estrategia para evitar el efecto Babel es crear una **matriz de traducción**:

| Técnico | Negocio | Qué significa |
|---|---|---|
| Latencia | Tiempo de respuesta | Cuánto tarda en responder el sistema |
| Throughput | Capacidad de atención | Cuántos usuarios simultáneos soporta |
| Failover | Continuidad operativa | Qué pasa si un servidor se cae |
| Deuda técnica | Mantenimiento pendiente | Trabajo que retrasa nuevas funciones |
| SLA | Nivel de servicio prometido | Qué compromiso tenemos con el cliente |
| Escalabilidad horizontal | Crecer sin mejorar hardware | Más servidores vs servidor más grande |
| Consistencia eventual | Puede tardar en actualizarse | Datos que no están sincronizados al instante |
| ACID | Transacción segura | Si falla algo, se revierte todo |

Esta matriz vive en la documentación del proyecto y se comparte con:
- El equipo de desarrollo
- Los stakeholders de negocio
- Los gestores de producto

### Ejemplo práctico

Si dices "tenemos problemas de consistencia eventual en la base de datos", el negocio no entiende.
Si dices "el usuario puede ver precios antiguos por unos segundos después de un cambio", todos entienden.

---

## Síntesis

1. **Conocer la gestión estructural** → define qué costos importan
2. **Saber por qué nos eligen** → define qué priorizar
3. **Trade-offs explícitos** → cada decisión tiene un costo de oportunidad
4. **Lenguaje común** → evitar el efecto Babel
5. **Matriz de traducción** → conectar técnico con negocio

> El arquitecto no solo diseña sistemas — diseña comunicación que permite que el sistema exista.

---

## Próximos temas

- [ ] ADR (Architectural Decision Records) — documentar decisiones con costos explícitos
- [ ] OKRs vs KPIs en arquitectura — cómo medir lo que importa
- [ ] Ejemplos reales de trade-offs en empresas conocidas
