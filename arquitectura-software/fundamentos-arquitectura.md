# Fundamentos de Arquitectura de Software

> Basado en notas de estudio sobre arquitectura de software. Voz propia, enfoque práctico.

---

## Contexto

El contexto es todo. Antes de proponer cualquier cosa, hay que entender el entorno:

**Qué incluye el contexto:**
- Requisitos: desde funcionales hasta no funcionales y riesgos
- Estrategia: saber qué riesgos implica
- Capacidades: ligadas a las restricciones existentes
- Equipo: saber si el equipo puede alcanzar la meta
- Tipo de empresa: el contexto también es saber dónde estás

**El tipo de empresa define el riesgo aceptable:**

| Tipo | Tolerancia al riesgo | Espacio para innovación |
|---|---|---|
| Startup | Riesgos grandes, innovación agresiva | Alto — se busca diferenciación |
| Micro empresa | Riesgo aceptable, pero no siempre se busca innovación | Limitado —活下去 primero |
| Compañía establecida | Complicado, innovación controlada | Medio — todo pasa por el ojo de todos |
| Empresa pública | No les gusta el riesgo | Bajo — cumplimiento y estabilidad |

> Entender esto evita proponer soluciones que la organización no puede absorber.

---

## Qué es diseñar software

Diseñar es una responsabilidad que implica desarrollar productos que le dan valor a una organización.

**Componentes del diseño:**
- Estilos arquitectónicos que llevan a abstracciones o contenedores
- Componentes: dónde viven, cómo se evalúan
- Dependencias, fronteras
- Métricas generadas para medir desempeño
- Patrones recomendados y pruebas
- Relación con el código, tests y documentación

**Herramientas de diseño:**
- TOGAF
- C4 Model
- Architectural Decision Record (ADR)
- Patrones de diseño
- Modelo de gestión de riesgo
- AI (para ayudar a convencer, no para reemplazar el juicio)

---

## Responsabilidades del Arquitecto

Arquitectura es una responsabilidad que genera cultura, tomando decisiones entre todos — lo que hace el arquitecto.

**Qué necesita un arquitecto internamente:**
- Generar productos de arquitectura
- Aplicar diseños consistentes
- Adaptarse a metodologías
- Hacer pruebas de concepto
- Registrar decisiones: el "por qué" al momento de resolver un problema

**Relación con metodología de desarrollo:**
El arquitecto no diseña en el vacío. Está atado a cómo el equipo construye software.

---

## Malas Prácticas

Estas son las trampas más comunes:

### 1. Ilusión de productividad
Entregar mucho, pero con baja calidad que no estaría aceptada para producción.
- Código que "funciona" pero no tolera el uso real
- Technical debt que frena al equipo después
- El metric驱动 es cantidad de features, no valor

### 2. Dependencia de un proveedor
Evitar depender de un agente o servicio externo — o se estará atrapado a sus cuerdas.
- Vendor lock-in de cloud, APIs, libraries
- Sin proveedor: libertad; con proveedor: negociar poder de bargaining

### 3. Résumé driven development
Priorizar logros personales en resultados del equipo y producto.
- "Esta tecnología está en trend, hay que ponerla"
- Decisiones basadas en el CV, no en el problema
- Stack que brilla en presentaciones pero complica mantenimiento

### 4. Parálisis por análisis
Cuando los desarrolladores no empiezan porque el arquitecto no ha tomado las decisiones de diseño.
- El equipo espera el OK del arquitecto para cada cosa
- Diseño perfecto que nunca llega → el equipo se frena
- Hay que saber cuándo el diseño está "suficientemente bien"

### 5. Sistemas infinitamente personalizables
Intentar ir más allá y solucionar problemas que no se presentan aún.
- Over-engineering por anticipar el futuro
- "Qué pasa si el usuario quiere hacer X" → se construye para X aunque nadie lo pida
- Abstracciones que no resuelven nada actual

---

## Fitness Functions

Para evitar las malas prácticas, usamos fitness functions — pruebas que verifican que la arquitectura cumple sus objetivos.

**Tipos dentro de estas:**
- **Métricas**: validar con datos que todo va según los objetivos de diseño
- **Pruebas unitarias en código**: validar que el código cumple con las decisiones tomadas y es funcional
- **Ingeniería del caos**: literalmente ir a golpear al servidor a ver si sobrevive — inundando la red, apagando partes, provocando fallos controlados
- **Monitoreo**: darle seguimiento a todo lo que se hace

---

## Ley de Conway

> Los sistemas generados reflejan la comunicación interna de la organización.

El arquitecto debe identificar el estilo de comunicación de la empresa para usarlo en sus documentos.

- Si la empresa tiene silos → la arquitectura va a terminar en silos
- Si hay colaboración interdisciplinaria → los equipos cruzan fronteras
- Si la comunicación es jerárquica → las decisiones fluyen de arriba hacia abajo

No es una opinión del arquitecto — es un diagnóstico.

---

## Espacio del Problema vs Espacio de la Solución

**Espacio del problema:**
- Indagación real con el cliente
- Preguntas del "por qué" o "para qué"
- Evitar asumir soluciones inmediatas en los requisitos
- Entender el contexto antes de hablar de tecnología

**Espacio de la solución:**
- Centrado en el "cómo se va a hacer"
- Las funcionalidades
- La implementación técnica

> El senior va directo al "cómo". El arquitecto se pregunta "por qué estamos resolviendo esto".

---

## Requisitos: Funcionales, No Funcionales, Impacto y Costos

### Requisitos funcionales
Son las funciones que el usuario puede ver, las lógicas de fondo, los permisos para visibilidad y la lógica detrás que resuelve el problema final del usuario, cumpliendo con el objetivo pactado.

### Requisitos no funcionales
Definen el alcance del software al llegar a producción:
- Seguridad
- Disponibilidad
- Escalabilidad
- Carga del sistema para uno o varios usuarios al mismo tiempo

### Impactos y costos
Toda decisión trae un impacto, y hay costos asociados que pueden variar o incrementarse.

### Matriz de restricciones
Permite priorizar, clasificar, mitigar o controlar las restricciones con base en el negocio, requiriendo comunicación directa con el equipo para solventarlas.

---

## Patrones Comunes en la Industria

### Estructura jerárquica o centralizada
La toma de decisiones fluye desde arriba.

### Estructura matricial
Promueve la colaboración interdisciplinaria.

### Equipos aislados (silos)
Dificultan la comunicación efectiva.

### Comunidades de práctica
Redes informales de intercambio de conocimiento.

---

## Comunicación con el Equipo

**Regla:** Las reuniones deben utilizarse para mostrar documentos construidos sobre plantillas alineadas con la cultura de la organización.

- Evitar el "está bien" sin feedback real
- Incentivar preguntas y objeciones
- Que los documentos vivan en templates, no en presentaciones de una vez

**Técnicas útiles:**
- **Cinco por qué**: iterar sobre el problema preguntando "por qué" cinco veces
- **Seis sombreros**: considerar múltiples perspectivas (datos, emociones, crítica, optimism, creatividad, overview)

---

## Próximos temas

- [ ] ADR (Architectural Decision Records) — documentar decisiones
- [ ] C4 Model — cómo usarlo para comunicar arquitectura
- [ ] Patrones arquitectónicos específicos (microservicios, monolith, event-driven)
- [ ] Métricas de arquitectura en código
- [ ] TOGAF — cuándo y cómo aplicarlo
