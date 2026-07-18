# Guion Extendido: Fundamentos de Arquitectura de Software

> **Propósito:** Material fuente completo y extenso para generar una presentación (slides) de un curso de **Fundamentos de Arquitectura de Software**. Este guion cubre en detalle todo el contenido de la carpeta `arquitectura-software/` del repositorio `Learning/`, e incluye además una sección dedicada a **cómo aplicar estos fundamentos en la empresa real** (costos de codificación, mejora de procesos, impacto en el negocio).
>
> **Cómo usar este archivo:**
> - **Opción A:** Cópialo completo en tu herramienta de IA (Gamma, Beautiful.ai, SlidesAI, Canva AI, etc.) y pídele que genere la presentación slide por slide. El archivo ya está estructurado con bloques `## SLIDE N` listos para usar.
> - **Opción B:** Úsalo como base para diseñar diapositivas manualmente, tomando los párrafos narrativos como contenido.
> - **Opción C:** Léelo directamente como guion hablado si vas a presentar tú.
>
> **Audiencia:** Estudiantes / developers con conocimientos básicos de programación que se inician en arquitectura de software, o equipos de desarrollo que quieren profesionalizar su forma de pensar el software.
>
> **Duración sugerida de la presentación:** 60-90 minutos (presentación completa).
>
> **Origen:** Notas del repositorio `Learning/arquitectura-software/` (David — 2026), con sección adicional sobre aplicación empresarial.

---

## 0. Contexto de la presentación

**Título sugerido:** *Fundamentos de Arquitectura de Software: de monolito a microservicios, de cliente-servidor a eventos*

**Subtítulo:** *Una introducción práctica al pensamiento arquitectónico: contexto, estilos, principios, decisiones y cómo aplicarlo en la empresa.*

**Mensaje central (lo que el alumno debe llevarse):**
> La arquitectura de software no es una decisión técnica aislada — es una decisión de negocio, equipo y contexto. Antes de elegir un estilo, un patrón o una tecnología, hay que entender el problema, la organización y a las personas que van a operar el sistema. Y una vez entendido, el siguiente paso es **llevar ese pensamiento arquitectónico a la práctica dentro de la empresa**, mejorando no solo el código, sino también los procesos, la comunicación, los costos y la velocidad con la que el equipo entrega valor.

**Temario general (índice de la presentación):**

1. ¿Qué es diseñar software? El rol del arquitecto
2. El contexto: requisito, equipo, organización
3. Requisitos: funcionales, no funcionales, costos
4. Cliente-servidor: la base de todo
5. Estilos de arquitectura: monolito → microservicios → eventos
6. Monolito: simple, poderoso y muchas veces suficiente
7. Arquitectura orientada a servicios: contratos que conectan
8. Microservicios: dividir para escalar
9. Arquitectura orientada a eventos: producir, consumir, reaccionar
10. Arquitectura limpia: círculos concéntricos y dependencias hacia adentro
11. Principios SOLID: las 5 reglas del diseño orientado a objetos
12. Cuándo usar un patrón (y cuándo no)
13. Costos, trade-offs y lenguaje común
14. Malas prácticas y fitness functions
15. Ley de Conway y comunicación
16. Serendipia, feedback y mejora continua
17. **Cómo aplicar estos fundamentos en la empresa real** (sección nueva)

---

## SLIDE 1 — Portada

**Título:** Fundamentos de Arquitectura de Software
**Subtítulo:** De monolito a microservicios · De cliente-servidor a eventos
**Pie de slide:** Curso introductorio · Basado en notas prácticas de la industria

**Guion extendido para el orador:**

Bienvenidos a este recorrido por los fundamentos de la arquitectura de software. A lo largo de esta sesión vamos a trabajar con un enfoque muy práctico: no vamos a quedarnos en definiciones teóricas, sino que vamos a conectar cada concepto con decisiones reales que toman los equipos de desarrollo todos los días. La arquitectura de software suena intimidante, pero en el fondo se trata de tomar buenas decisiones sobre cómo organizar el código, los equipos y la tecnología. Vamos a recorrer desde los conceptos más básicos — como cliente-servidor o monolito — hasta principios de diseño como SOLID o la arquitectura limpia, y cerraremos con una parte muy importante: cómo llevar todo este conocimiento a la práctica dentro de una empresa, cómo mejorar los procesos y cómo reducir costos de desarrollo. La idea es que al terminar esta sesión, tengas un mapa mental claro para tomar mejores decisiones técnicas y empresariales.

---

## SLIDE 2 — ¿Qué es diseñar software?

**Título:** Diseñar software: una responsabilidad, no un documento

**Bullets clave:**
- Diseñar software es **desarrollar productos que generan valor** para una organización.
- Implica tomar decisiones sobre estilos arquitectónicos, componentes, dependencias, fronteras y métricas.
- No se trata solo de "elegir tecnología" — se trata de **organizar el código para que sobreviva al cambio**.

**Componentes del diseño:**
- Estilos arquitectónicos que llevan a abstracciones o contenedores.
- Componentes: dónde viven, cómo se evalúan.
- Dependencias y fronteras claras.
- Métricas para medir desempeño.
- Patrones recomendados y pruebas.
- Relación con el código, los tests y la documentación.

**Herramientas comunes del arquitecto:**
- TOGAF (framework de arquitectura empresarial).
- C4 Model (diagramas por niveles).
- ADR (Architectural Decision Records).
- Patrones de diseño.
- Modelo de gestión de riesgo.
- AI como asistente (para ayudar a convencer, no para reemplazar el juicio).

**Guion extendido para el orador:**

Empecemos por lo más básico: ¿qué significa realmente diseñar software? La palabra "diseño" a veces se malentiende. Diseñar no es sentarse a dibujar diagramas bonitos en una herramienta, ni tampoco es simplemente elegir un framework o una base de datos. Diseñar software es una responsabilidad. Es el acto de tomar decisiones técnicas que van a impactar directamente en el valor que la organización entrega a sus usuarios y clientes. Cuando un arquitecto o un senior diseña un sistema, está decidiendo cómo van a interactuar los componentes, dónde van a vivir las responsabilidades, qué dependencias van a existir entre unas partes y otras, cómo se van a medir los resultados, y cómo va a evolucionar ese sistema con el tiempo. Lo más interesante de diseñar es que no es un evento: es un proceso continuo. El diseño se hace, se mide, se ajusta y se vuelve a hacer. Por eso herramientas como los ADRs (Architectural Decision Records) son tan valiosas: nos permiten registrar el "por qué" de cada decisión, para que dentro de seis meses, cuando alguien nuevo llegue al equipo, pueda entender el razonamiento que llevó a esa decisión y no termine repitiendo los mismos errores. Un buen diseño sobrevive al paso del tiempo. Un mal diseño, tarde o temprano, se cae — y cuando se cae, lo hace en el peor momento: en producción, con usuarios reales, con dinero real en juego.

---

## SLIDE 3 — El rol del arquitecto

**Título:** El arquitecto: decisiones + cultura

**Bullets clave:**
- La arquitectura **genera cultura**: es el resultado de decisiones tomadas entre todos.
- El arquitecto no es un ente aislado: **trabaja con el equipo**.
- Su trabajo es entregar productos de arquitectura consistentes y adaptados a la metodología del equipo.

**Responsabilidades internas del arquitecto:**
- Generar productos de arquitectura (documentos, ADRs, diagramas).
- Aplicar diseños consistentes.
- Adaptarse a la metodología de desarrollo del equipo.
- Hacer pruebas de concepto antes de comprometer decisiones grandes.
- **Registrar decisiones** (el "por qué" al momento de resolver un problema).

**Herramientas comunes del arquitecto:**
- TOGAF (framework de arquitectura empresarial).
- C4 Model (diagramas por niveles).
- ADR (Architectural Decision Records).
- Patrones de diseño.
- Modelo de gestión de riesgo.
- AI como asistente (para ayudar a convencer, no para reemplazar el juicio).

**Guion extendido para el orador:**

El rol del arquitecto de software está rodeado de mitos. Algunos piensan que es la persona que sabe más de tecnología y decide todo desde un trono. Otros piensan que es un cargo puramente decorativo. La realidad está en el medio. Un arquitecto de software es, ante todo, alguien que **toma decisiones técnicas con impacto organizacional**. Genera cultura, y no lo hace solo: lo hace con el equipo. La arquitectura no es un documento en una wiki que nadie lee; es el resultado de conversaciones, pruebas, errores y aciertos compartidos. Entre las responsabilidades internas más importantes está la de registrar decisiones. Esto es crítico. Un buen ADR es como una fotografía del momento en que se tomó una decisión: qué alternativas se consideraron, qué se eligió, por qué se eligió, y qué trade-offs se aceptaron. Esto evita que el equipo vuelva a discutir los mismos puntos cada vez que entra alguien nuevo, o cada vez que hay un cambio de contexto. La arquitectura tampoco se diseña en el vacío: está atada a la metodología de desarrollo del equipo. No es lo mismo diseñar para un equipo que trabaja en cascada que para uno que trabaja en Scrum, Kanban o XP. El arquitecto debe adaptarse a cómo el equipo construye software, no al revés. Y por último, la AI se ha convertido en una herramienta muy útil para el arquitecto moderno: ayuda a contrastar ideas, a explorar alternativas, a stressear diseños. Pero siempre como asistente, nunca como reemplazo del juicio humano. La AI puede equivocarse, pero la responsabilidad final es del arquitecto.

---

## SLIDE 4 — El contexto es todo

**Título:** Antes de proponer, entiende el contexto

**Bullets clave:**
- El **contexto** es el entorno completo del problema: requisitos, estrategia, equipo, organización.
- Si no entiendes el contexto, cualquier propuesta es un tiro al aire.

**Qué incluye el contexto:**
- **Requisitos**: funcionales, no funcionales y riesgos.
- **Estrategia**: qué riesgos acepta la organización.
- **Capacidades**: ligadas a las restricciones existentes.
- **Equipo**: ¿puede alcanzar la meta?
- **Tipo de empresa**: el contexto también es saber dónde estás.

**Tabla: tipo de empresa vs. tolerancia al riesgo**

| Tipo de empresa | Tolerancia al riesgo | Espacio para innovación |
|---|---|---|
| Startup | Riesgos grandes | Alto — diferenciación |
| Micro empresa | Riesgo aceptable, sin innovar siempre | Limitado — sobrevivir primero |
| Compañía establecida | Innovación controlada | Medio — pasa por muchos ojos |
| Empresa pública | No les gusta el riesgo | Bajo — cumplimiento y estabilidad |

**Guion extendido para el orador:**

Este es probablemente el concepto más importante de toda la sesión. Si te llevas una sola cosa, que sea esta: **antes de proponer cualquier solución técnica, entiende el contexto**. Y el contexto no es solo "qué quiere el cliente". El contexto es el ecosistema completo. Incluye los requisitos — tanto los funcionales como los no funcionales, y los riesgos asociados. Incluye la estrategia de la organización: ¿está en modo exploración buscando un nuevo mercado, o está en modo consolidación defendiendo su posición? Incluye las capacidades reales: ¿qué tiene hoy la empresa? ¿Con qué tecnología cuenta? ¿Con qué presupuesto? ¿Con qué equipo? Y por supuesto, incluye el equipo humano: ¿tiene la madurez para ejecutar la solución que estoy proponiendo? Por último, incluye el tipo de empresa, que es un factor determinante. Una startup puede permitirse tomar riesgos grandes porque busca diferenciación agresiva en el mercado. Una microempresa necesita sobrevivir primero, así que el espacio para innovar es limitado. Una compañía establecida, con múltiples stakeholders y años de historia, requiere innovación controlada que pase por muchos ojos. Y una empresa pública, donde lo que prima es el cumplimiento normativo y la estabilidad, no tolera bien el riesgo. Entender esto evita una trampa muy común: proponer soluciones brillantes técnicamente que la organización simplemente no puede absorber. Una arquitectura de microservicios perfecta en una empresa con un equipo de tres personas y cero madurez operacional no es innovación, es responsabilidad. El contexto manda. Siempre.

---

## SLIDE 5 — Requisitos: funcionales, no funcionales, costos

**Título:** No todo requisito es visible para el usuario

**Bullets clave:**

**Requisitos funcionales:**
- Las funciones que el usuario puede ver.
- Las lógicas de fondo.
- Los permisos para visibilidad.
- La lógica que resuelve el problema final del usuario.

**Requisitos no funcionales:**
- Definen el alcance del software al llegar a producción.
- Seguridad.
- Disponibilidad.
- Escalabilidad.
- Carga del sistema para uno o varios usuarios simultáneos.

**Impactos y costos:**
- Toda decisión trae un impacto.
- Los costos asociados pueden variar o incrementarse con el tiempo.

**Matriz de restricciones:**
- Permite priorizar, clasificar, mitigar o controlar las restricciones según el negocio.
- Requiere comunicación directa con el equipo para resolverlas.

**Guion extendido para el orador:**

Cuando un cliente o un product owner te pide "quiero un sistema que haga X", ese X es la punta del iceberg. Debajo hay mucho más, y de eso depende que el sistema sobreviva en producción. Los requisitos funcionales son los más fáciles de identificar: son las funciones visibles, los flujos que el usuario ejecuta, la lógica que resuelve el problema. Un carrito de compras, un sistema de login, un formulario de pago: todo eso es funcional. Pero los requisitos no funcionales son los que definen si tu sistema va a funcionar mañana cuando tengas 10.000 usuarios en vez de 10. Son la seguridad, la disponibilidad, la escalabilidad, el rendimiento bajo carga. Un sistema puede cumplir perfectamente todos los requisitos funcionales y aun así ser un desastre en producción porque no contempló la concurrencia, los picos de tráfico, la latencia de red, las vulnerabilidades de seguridad. La diferencia entre un sistema "que funciona en el localhost" y uno "que funciona en producción" son los requisitos no funcionales. Y cada decisión arquitectónica tiene un impacto, y por lo tanto un costo. Cambiar de una base de datos relacional a una NoSQL tiene un costo. Migrar a microservicios tiene un costo. Adoptar un nuevo framework tiene un costo. Estos costos no son solo monetarios: son también de tiempo, de aprendizaje, de riesgo de fallos durante la transición. Por eso existe la matriz de restricciones: una herramienta que permite priorizar, clasificar, mitigar o controlar cada restricción según el peso que tenga en el negocio. Pero ojo: esa matriz no se construye sola. Requiere comunicación directa con el equipo, con el product owner, con los stakeholders. Si la matriz la hace el arquitecto en un rincón sin consultar, va a estar desconectada de la realidad.

---

## SLIDE 6 — Espacio del problema vs. espacio de la solución

**Título:** Senior piensa en el "cómo". Arquitecto piensa en el "por qué"

**Dos columnas:**

**Espacio del problema:**
- Indagación real con el cliente.
- Preguntas del "por qué" o "para qué".
- Evitar asumir soluciones inmediatas en los requisitos.
- Entender el contexto antes de hablar de tecnología.

**Espacio de la solución:**
- Centrado en el "cómo se va a hacer".
- Las funcionalidades.
- La implementación técnica.

**Frase para recordar:**
> *"El senior va directo al 'cómo'. El arquitecto se pregunta 'por qué estamos resolviendo esto'."*

**Guion extendido para el orador:**

Hay una diferencia enorme entre un developer senior y un arquitecto de software, y esa diferencia se ve perfectamente en cómo abordan un problema nuevo. Cuando a un senior le dicen "necesito un sistema de notificaciones", el senior piensa: "¿qué canal uso? ¿email, push, SMS? ¿Qué base de datos? ¿Qué broker?". Va directo al "cómo". Eso está bien: el senior es ejecutor, y necesita ejecutar. Pero el arquitecto se hace otra pregunta primero: **¿por qué necesitamos un sistema de notificaciones? ¿Qué problema del usuario estamos resolviendo? ¿Estamos seguros de que la notificación es la solución correcta?** A veces el problema real es otro. A veces la notificación es solo un parche para un problema más profundo. El espacio del problema es el lugar donde se hace esa indagación. Es donde se hacen preguntas incómodas, donde se evita asumir soluciones inmediatas. Es donde se valida con el cliente qué es lo que realmente necesita, no lo que dice que necesita. Y solo después de entender bien el problema, pasamos al espacio de la solución: el "cómo se va a hacer". Las funcionalidades, la implementación técnica, los componentes. El arquitecto que se queda en el espacio de la solución sin pasar por el espacio del problema termina construyendo el sistema equivocado. Y lo construye perfectamente, con código limpio, tests, documentación... pero resuelve un problema que no era el real. El arte está en dominar ambos espacios: entender profundamente el problema para luego elegir la mejor solución técnica. Ni quedarse en la teoría sin construir nada, ni lanzarse a programar sin entender qué se está construyendo.

---

## SLIDE 7 — Cliente-servidor: la base de todo

**Título:** La conexión que lo empezó casi todo

**Concepto clave:**
- La conexión cliente-servidor es **bidireccional**: el cliente habla con el servidor, pero el servidor también puede iniciar comunicación cuando tiene algo que entregar.
- Antes de hablar de SPA, SSR, micro-frontends o BFF, hay que entender este fundamento.

**Dos tipos de cliente:**

**Cliente rico (fat client):**
- Tiene lógica dentro. Procesa eventos localmente antes de enviar al servidor.
- Flujo: usuario interactúa → cliente procesa → envía evento procesado → servidor corrobora → responde.
- Respuesta inmediata en la interfaz.
- Mayor complejidad en el cliente.
- Ejemplo: aplicaciones de escritorio con lógica de negocio.

**Cliente ligero (thin client):**
- Se puede representar como solo la parte visual. Encargado de eventos, sin lógica.
- Flujo: usuario interactúa → cliente lanza la llamada → servidor procesa todo → devuelve resultado → cliente solo renderiza.
- Lógica centralizada en el servidor.
- Mayor latencia percibida en operaciones complejas.
- Ejemplo: aplicaciones web tradicionales.

**Ejemplo clásico — la app web:**
1. El navegador envía eventos al servidor.
2. El servidor procesa la lógica.
3. El servidor consulta la base de datos.
4. Devuelve el resultado.
5. El usuario lo ve en el cliente.

**Guion extendido para el orador:**

Antes de hablar de las modas modernas — Single Page Applications, Server-Side Rendering, micro-frontends, Backend for Frontend — hay que volver a los fundamentos. Y el fundamento de casi todo lo que hacemos en la web es el modelo cliente-servidor. La idea es simple: hay un cliente (la aplicación que usa el usuario) y un servidor (la máquina que procesa la lógica y guarda los datos). La comunicación entre ambos es bidireccional: el cliente puede pedirle cosas al servidor, pero el servidor también puede iniciar la comunicación cuando tiene algo que entregar, como una notificación push o un mensaje en tiempo real. Ahora, no todos los clientes son iguales. Hay dos tipos fundamentales. El cliente rico, o fat client, es aquel que tiene lógica dentro. Procesa eventos localmente, valida datos, transforma información antes de enviarla al servidor. Piensa en una aplicación de escritorio tradicional, como una app de edición de video o un juego: gran parte del trabajo se hace en tu máquina, y solo cuando es necesario se sincroniza con el servidor. Esto da respuesta inmediata en la interfaz y menor carga en el servidor, pero el cliente se vuelve más complejo. Por otro lado, el cliente ligero, o thin client, es prácticamente solo la parte visual. Captura eventos del usuario y los envía al servidor, donde se procesa todo. El servidor devuelve el resultado y el cliente solo lo renderiza. Piensa en una aplicación web tradicional: el navegador no hace casi nada, solo muestra lo que el servidor le manda. ¿Cuál es mejor? Depende. El cliente rico da mejor experiencia de usuario en operaciones complejas; el cliente ligero es más simple de mantener y centraliza la lógica. La clave es entender estos dos modelos puros antes de entrar en las variantes modernas. Quien entiende cliente rico y cliente ligero en su forma pura, puede entender cualquier variante moderna — SPA, SSR, BFF — con mucho menos esfuerzo. Las modas vienen y van, pero estos dos conceptos siguen siendo la base.

---

## SLIDE 8 — Estilos de arquitectura: el panorama general

**Título:** No hay estilo perfecto. Hay estilo correcto para tu contexto

**Frase para recordar:**
> *"No existe el estilo perfecto. Existe el estilo que tu organización puede operar hoy sin convertirse en caos."*

**La regla de oro antes de elegir:**
- Conoce correctamente el **espacio del problema**.
- Las restricciones del problema deben estar claras.
- Si no las conoces, cualquier propuesta es un tiro al aire.

**Los 5 estilos principales (en orden de progresión sugerida):**

1. **Monolito** — todo en un solo proceso, un solo deploy.
2. **Monolito restringido por el problema** — fronteras internas dictadas por el dominio.
3. **Monolito modular** — mismo deploy, módulos separados.
4. **Microservicios** — servicios independientes que escalan por separado.
5. **Servicios basados en eventos** — comunicación asíncrona por eventos.

**Progresión sugerida:**
```
Monolito → Monolito restringido → Monolito modular → Microservicios → Eventos
```

**Factores para decidir cuándo avanzar:**
- Madurez del equipo para operar y monitorear.
- Claridad del dominio y sus fronteras.
- Necesidades reales de escalamiento.
- Restricciones de la organización.

**Guion extendido para el orador:**

Ahora sí, vamos a entrar en los estilos de arquitectura. Pero antes de verlos, una advertencia: no hay un estilo mejor en abstracto. No existe el "mejor estilo" como categoría universal. Lo que existe es el estilo correcto para un contexto, una organización y un equipo específicos. Un estilo que funciona perfectamente en Netflix puede ser una ruina en una empresa local de Yumbo. La decisión entre estilos no es técnica en primer lugar — es organizacional. Dicho esto, sí hay una progresión lógica que la industria ha ido descubriendo con los años, y que va de menor a mayor complejidad operativa. Empezamos con el monolito, que es la forma más simple: todo en un solo proceso, un solo deploy. Es ideal para equipos pequeños, problemas bien entendidos y estabilidad. Después viene el monolito restringido por el problema, donde las restricciones del negocio definen las fronteras internas, no la tecnología. Esto significa que separamos el código no porque sea elegante, sino porque el dominio lo pide. Luego está el monolito modular, que es el mismo deploy pero con módulos claramente separados que algún día podrían extraerse. Es el paso intermedio natural antes de dar el salto a microservicios. Microservicios son servicios independientes, cada uno con su propio proceso, su propia base de datos y su propio ciclo de deploy. Requieren madurez operativa alta, dominio bien delimitado y necesidad real de escalamiento independiente. Y finalmente están los servicios basados en eventos, donde la comunicación es asíncrona y los servicios reaccionan a hechos que ya ocurrieron. Esta progresión no es rígida. No todos los proyectos la siguen paso a paso. Hay sistemas que nacen como microservicios porque el problema realmente lo exige. Hay monolitos que viven décadas con orgullo. La clave está en preguntarse: ¿qué puede operar mi organización hoy sin que se convierta en caos? Esa pregunta vale más que cualquier framework de moda.

---

## SLIDE 9 — Monolito

**Título:** Monolito: simple, poderoso y muchas veces suficiente

**Definición:**
- Estilo de arquitectura donde **toda la aplicación vive en un solo proceso**.
- Un solo deploy.
- Comparable con un videojuego: instalas una vez y todo está contenido.

**Módulos dentro del monolito:**
- No significa que todo esté en un solo archivo.
- Podemos tener **módulos** que separan secciones lógicas.
- Agilidad al hacer cambios porque el código está organizado.
- A la hora de desplegar sigue siendo todo junto.

**Ventajas:**
- Simples de manejar: una sola codebase, un solo deploy.
- Fáciles en equipos pequeños: sin complejidad operacional.
- Rollback simple: un solo deploy hacia atrás lo revierte todo.
- Comunicación en memoria: llamadas directas entre módulos, sin red.

**Desventajas:**

*"Todo a la vez o nada":*
- Un cambio requiere desplegar todo.
- Equipos esperando deploy mientras otros están en testing — el día a día de un monolito grande.

*Ruido entre módulos (noisy neighbor):*
- Un módulo consume muchos recursos y afecta a los demás.
- Si la base de datos es monolítica, el problema persiste aunque el código esté modularizado.

*Cuanto más crece, más duele:*
- Tiempos de inicio más largos.
- Tests más lentos.
- Coordinación entre equipos que tocan el mismo código se complica.

**Cuándo considerar un monolito:**
- Equipos pequeños.
- Problemas bien entendidos y estables.
- Necesidad de simplicidad operativa.
- La organización aún no tiene madurez para sistemas distribuidos.

**Frase para recordar:**
> *"No es malo partir de un monolito. Es malo quedarse en un monolito sin módulos cuando el dominio ya pide separación."*

**Guion extendido para el orador:**

El monolito es probablemente el estilo de arquitectura más malentendido. Muchos developers junior y muchos managers lo ven como algo "viejo" o "mal hecho", como un paso que hay que dar rápido para llegar a microservicios. La realidad es muy distinta. Un monolito es un estilo de arquitectura donde toda la aplicación vive en un solo proceso. Un solo deploy. Piensa en un videojuego: lo instalas una vez y todo está contenido. Pero ojo: monolito no significa "código en un solo archivo gigante". Eso sería un monolito mal hecho. Un buen monolito tiene módulos internos que separan secciones lógicas del código, cada uno con su propia responsabilidad. La organización del código te da agilidad al hacer cambios, pero a la hora de desplegar sigue siendo todo junto. Las ventajas son muchas. Es simple de manejar: una sola codebase, un solo deploy. Es fácil en equipos pequeños: no hay complejidad operacional significativa. El rollback es simple: si algo falla, un solo deploy hacia atrás lo revierte todo. Y la comunicación entre módulos es en memoria, sin latencia de red, lo que hace que las operaciones internas sean rápidas. Pero también tiene desventajas serias. La primera es "todo a la vez o nada": si necesitas cambiar una sola línea, despliegas todo el sistema. Esto genera cuellos de botella cuando varios equipos quieren desplegar a la vez. La segunda es el "noisy neighbor": un módulo que hace mucho trabajo pesado puede agotar los recursos del proceso y afectar a todos los demás usuarios. Y la tercera es que cuanto más crece, más duele: los tiempos de inicio se alargan, los tests se vuelven más lentos, y la coordinación entre equipos que tocan el mismo código se complica. ¿Cuándo conviene un monolito? Cuando tienes equipos pequeños, problemas bien entendidos y estables, y necesidad de simplicidad operativa. El monolito bien hecho — con módulos claros y fronteras definidas — es el calentamiento perfecto para microservicios. Las fronteras que defines dentro del monolito son las mismas que vas a necesitar después. No es malo partir de un monolito. Es malo quedarse en un monolito sin módulos cuando el dominio ya pide separación.

---

## SLIDE 10 — Arquitectura orientada a servicios (SOA)

**Título:** Sin contrato, no hay comunicación

**Concepto central:**
- Todo gira alrededor de un **contrato** entre cliente y servidor.
- El cliente no se conecta libremente — envía un contrato que dicta:
  - A qué servidores puede conectarse.
  - Cómo debe ser la comunicación.
  - Qué operaciones están disponibles.
- Sin contrato válido, no hay conexión. **Todo o nada.**

**SOAP — el contrato estricto:**
- XML como lenguaje de intercambio.
- WSDL (Web Services Description Language) como manual de reglas.
- La conexión solo se da si el contrato está 100% correcto.
- Contratos extremadamente detallados y predecibles.

**¿Por qué SOAP sigue vivo?**
- Su rigidez no es debilidad — es su fortaleza.
- Se usa en sectores donde un error de formato tiene consecuencias legales o financieras:
  - Sistemas financieros (bancos, bolsas).
  - Salud (historias clínicas, seguros).
  - Gobierno (trámites, certificaciones).

**OpenAPI — el contrato moderno en REST:**
- OpenAPI Specification (OAS) es el estándar para APIs REST modernas.
- Dicta: endpoints, métodos HTTP, formato de request/response, autenticación, tipos de datos, ejemplos.
- REST API es el hijo moderno que sigue estas reglas de contrato.

**Swagger vs. OpenAPI — la distinción correcta:**

| Nombre | Qué es |
|---|---|
| OpenAPI Specification | La especificación formal (3.0, 3.1) — el estándar |
| Swagger | El ecosistema de herramientas de SmartBear |
| Swagger UI | Visor web para explorar la API documentada |
| Swagger Editor | Editor en navegador para escribir contratos |
| Swagger Codegen | Genera código cliente/servidor desde un contrato |

**Analogía final:**
- WSDL = contrato completo en SOAP.
- OpenAPI = contrato en REST moderno.
- Swagger = herramientas que implementan y visualizan ese contrato.

**Guion extendido para el orador:**

La arquitectura orientada a servicios tiene un concepto central que la define: el contrato. Todo gira alrededor de un contrato entre el cliente y el servidor. El cliente no se conecta libremente a un servidor — primero envía un contrato que dicta a qué servidores puede conectarse, cómo debe ser la comunicación y qué operaciones están disponibles. Sin un contrato válido, no hay conexión. Es todo o nada. Esta idea de "contrato" se ha materializado de distintas formas a lo largo de la historia, y dos de las más importantes son SOAP y OpenAPI. SOAP, que significa Simple Object Access Protocol, es el estándar más riguroso. Usa XML como lenguaje de intercambio y WSDL (Web Services Description Language) como manual de reglas. La conexión solo se establece si el contrato está 100% correcto: una firma mal, un dato mal escrito, y todo falla. Esta rigidez suena molesta, pero es su fortaleza. SOAP sigue vivo y se usa masivamente en sectores donde un error de formato puede tener consecuencias legales o financieras: sistemas bancarios, historias clínicas electrónicas, sistemas gubernamentales, aseguradoras. Cuando necesitas garantías absolutas de que el mensaje que envías es exactamente el mensaje que el receptor espera, SOAP entrega eso. Por otro lado, tenemos OpenAPI Specification, que es el estándar moderno para APIs REST. OpenAPI dicta cómo debe estructurarse una API: endpoints, métodos HTTP permitidos, formato de request y response, autenticación, tipos de datos, ejemplos de uso. REST API es el hijo moderno que sigue estas reglas. Ahora, es muy común confundir Swagger con OpenAPI, y no son lo mismo. OpenAPI es la especificación formal — el estándar en sí, en sus versiones 3.0 y 3.1. Swagger es el ecosistema de herramientas de SmartBear que implementa ese estándar. Swagger UI es el visor web que permite ver e interactuar con la API documentada. Swagger Editor es el editor en navegador. Swagger Codegen genera código automáticamente desde el contrato. La historia es interesante: Swagger fue creado por SmartBear como especificación, y en 2016 lo donaron a la Linux Foundation, donde se renombró a OpenAPI. Swagger sigue existiendo como marca comercial de las herramientas, pero el estándar se llama OpenAPI. Piensa en la analogía: WSDL es el contrato en SOAP, OpenAPI es el contrato en REST moderno, y Swagger son las herramientas que te permiten visualizar y trabajar con ese contrato. La regla inquebrantable se mantiene: en una arquitectura orientada a servicios, sin contrato no hay comunicación. El contrato es la ley.

---

## SLIDE 11 — Microservicios

**Título:** Microservicios: dividir para escalar (con cabeza)

**Fundamentos:**
- Dividir la aplicación en **pequeños servicios o módulos concretos**.
- Cada servicio es independiente de los demás y se encarga de una función específica.
- A diferencia del monolito, cada microservicio tiene:
  - Su propio proceso.
  - Su propia base de datos (idealmente).
  - Su propio ciclo de desarrollo y deploy.

**Gestión de contratos:**
- Es fundamental establecer **contratos bien definidos y claros** para las conexiones entre servicios.
- Un contrato bien definido permite que cada servicio evolucione sin romper las integraciones.

**Costos operativos y de producción:**
- No solo en el desarrollo inicial — el costo operacional continuo importa.
- Cada servicio debe estar conectado, monitorizado y desplegado de forma independiente.
- Costos que se agregan:
  - **Infraestructura** — compute, memoria, red por cada servicio.
  - **Mantenimiento** — más servicios significan más cosas que pueden fallar.
  - **Personal** — gente que sepa manejar sistemas distribuidos, redes, orquestación, contenedores.

**Síncrona vs. Asíncrona:**

*Síncrona:* un servicio llama a otro y espera la respuesta. Si el llamado falla, el que llama también se ve afectado. Puede generar bucles en cascada.

*Asíncrona (preferida):* el servicio que envía no espera respuesta. Envía el evento y continúa. El consumidor procesa cuando puede. El uso de **buffers como Kafka** es fundamental: si un servicio baja, el evento queda en el broker hasta que esté disponible.

**Patrón CQRS:**
- Command Query Responsibility Segregation.
- Separa las operaciones de **escritura (comandos)** de las de **lectura (consultas)**.
- En microservicios: escrituras en BD transaccional + lecturas en proyecciones actualizadas asíncronamente.

**Antes de ir a microservicios, pregúntate:**
- ¿El dominio está lo suficientemente maduro para identificar fronteras claras?
- ¿El equipo tiene madurez operativa para manejar múltiples servicios?
- ¿La organización puede absorber el costo de infraestructura y personal?
- ¿El problema realmente requiere independencia de despliegue y escalamiento?

**Guion extendido para el orador:**

Microservicios. La palabra mágica de la industria. Todo el mundo quiere trabajar con microservicios, todo el mundo quiere poner microservicios en su CV, todo el mundo quiere migrar su monolito a microservicios. Pero la realidad es que microservicios no son la respuesta a todo. Son una herramienta poderosa para problemas específicos, y usados en el contexto equivocado, se convierten en una pesadilla operativa. Vamos por partes. Los microservicios consisten en dividir la aplicación en pequeños servicios o módulos concretos. Cada servicio es independiente y se encarga de una función específica. A diferencia del monolito, cada microservicio tiene su propio proceso, su propia base de datos (idealmente) y su propio ciclo de desarrollo y deploy. Esto permite que cada servicio evolucione de forma independiente. El gran tema es la gestión de contratos. Es fundamental establecer contratos bien definidos y claros para las conexiones entre servicios. Un contrato bien definido permite que cada microservicio pueda evolucionar sin romper las integraciones con los otros. Un cambio interno en un servicio no debería afectar a sus consumidores si el contrato se respeta. Ahora hablemos de dinero, que es donde muchos se tropiezan. Los microservicios no son caros solo en el desarrollo inicial. Son caros de operar, todos los días. Cada servicio debe estar conectado a la nube o a un servidor independiente, monitorizado individualmente, desplegado de forma independiente. Esto agrega costos de infraestructura, costos de mantenimiento y costos de personal. Se necesita gente que sepa manejar sistemas distribuidos, redes, orquestación, contenedores. El monolito es barato de operar. Los microservicios son caros de operar. La pregunta no es "¿microservicios o no?" sino "¿puedo permitirme operarlos?". Un tema técnico clave es la comunicación. La síncrona, donde un servicio llama a otro y espera la respuesta, es peligrosa: si el servicio llamado falla, el que llama también se ve afectado, y se pueden generar bucles en cascada que tiren todo el sistema. La asíncrona, preferida, usa eventos o streams. El servicio que envía no espera respuesta, continúa su trabajo, y el consumidor procesa cuando puede. El uso de brokers como Kafka es fundamental: si un servicio baja, el evento queda en el broker hasta que esté disponible de nuevo. Un patrón muy útil en este contexto es CQRS (Command Query Responsibility Segregation), que separa las operaciones de escritura de las de lectura, creando modelos optimizados para cada caso. Antes de lanzarte a microservicios, hazte cuatro preguntas: ¿El dominio está lo suficientemente maduro para identificar fronteras claras? ¿El equipo tiene madurez operativa? ¿La organización puede absorber el costo? ¿El problema realmente requiere independencia de despliegue y escalamiento? Si la respuesta a cualquiera es "no", considera partir de un monolito modular. Los microservicios resuelven un problema de escala organizacional y técnica. Si no tienes ese problema, el monolito es la mejor opción.

---

## SLIDE 12 — Arquitectura orientada a eventos

**Título:** Producir, consumir y reaccionar

**Concepto central:**
- Un evento representa **una acción que ya sucedió** y que espera ser procesada.
- A diferencia de una llamada, el cliente **no espera**. Emite el evento y sigue.
- El procesamiento ocurre después, de forma asíncrona.

**Qué lleva un evento (nada más, nada menos):**
- Qué pasó — el tipo de evento.
- A quién va dirigido — el identificador del destinatario.
- Qué dato se necesita para procesarlo — un ID, una referencia, no todo el payload.

**Productores y consumidores:**
- **Producer**: genera el evento y lo envía. No sabe quién lo consume.
- **Consumer**: recibe el evento y lo procesa. No sabe quién lo emitió.
- No se conocen entre sí. **Eso es el desacoplamiento.**

**El buffer en medio (broker):**
- Kafka, RabbitMQ, SQS, etc.
- El producer envía al broker.
- El broker lo almacena en cola o topic.
- El consumer lo lee cuando puede.
- Permite que múltiples consumidores escuchen el mismo evento.

**Relación con DDD (Domain-Driven Design):**
- **Contexto delimitado**: el problema se divide en dominios pequeños y separados.
- **Eventos como resultado de cambios de estado**: cuando el modelo cambia, eso genera el evento.
- **Un concepto puede vivir en varios contextos**: la `Factura` existe en Ventas y en Contabilidad.

**Retos de esta arquitectura:**

*1. Flujo de tiempo entre eventos y contexto:* inconsistencias temporales.

*2. Eventos entrelazados:* orden y dependencias entre eventos.

*3. Consistencia eventual:* el sistema no garantiza actualización inmediata.

*4. Dificultad en el equipo:* entender el negocio desde eventos y contextos requiere capacitación.

**Cuándo considerar esta arquitectura:**
- La reacción a algo que pasó es más importante que el flujo directo.
- Necesidad de desacoplar productores de consumidores.
- Auditoría y trazabilidad de estado.
- Múltiples sistemas que necesitan reaccionar al mismo hecho.
- Escalabilidad independiente de productores y consumidores.

**Frase para recordar:**
> *"La pregunta no es '¿cuándo llegó?' sino '¿qué debe pasar cuando llegue?'"*

**Guion extendido para el orador:**

La arquitectura orientada a eventos es probablemente la más elegante y la más difícil de hacer bien al mismo tiempo. Su concepto central es simple: un evento representa una acción que ya sucedió, y está esperando a ser procesada. A diferencia de una llamada síncrona donde el cliente pide y espera respuesta, en la arquitectura orientada a eventos el cliente no espera. Emite el evento y sigue su vida. El procesamiento ocurre después, de forma asíncrona. Esto cambia completamente la forma de pensar un sistema. En vez de "¿qué le pido al servidor?", la pregunta es "¿qué pasó y quién necesita saberlo?". Un evento debe llevar lo mínimo necesario para procesarse. Nada más. ¿Qué pasó? El tipo de evento. ¿A quién va dirigido? El identificador del destinatario. ¿Qué dato se necesita? Un ID, una referencia, no todo el payload. Por ejemplo, un evento `FacturaEmitida` lleva el `factura_id` y el `cliente_id`. No lleva toda la factura. El consumidor, al recibir el evento, ya sabe a dónde dirigir el procesamiento y qué información adicional buscar si la necesita. La separación entre productores y consumidores es lo que da el desacoplamiento. El productor genera el evento y lo envía, pero no sabe quién lo va a consumir. El consumidor recibe el evento y lo procesa, pero no sabe quién lo emitió. No se conocen. Y entre ellos hay un broker — Kafka, RabbitMQ, SQS — que hace de muro. El productor envía al broker, el broker lo almacena, y el consumidor lo lee cuando puede. Esto permite que el sistema escale de forma independiente, que múltiples consumidores reaccionen al mismo evento para distintos propósitos, y que si un servicio baja, los eventos queden guardados hasta que se recupere. Esta arquitectura se basa mucho en DDD (Domain-Driven Design), y hay conceptos clave que vale la pena entender. El contexto delimitado divide el problema en dominios pequeños y separados. Los eventos son resultado de cambios de estado: cuando una entidad cambia, eso genera el evento. Y un mismo concepto puede vivir en varios contextos: la Factura existe en Ventas y en Contabilidad, y el evento `FacturaEmitida` cruza ambos contextos, pero cada uno lo interpreta según sus propias reglas. Ahora, los retos son reales. El flujo de tiempo entre eventos y contexto puede generar inconsistencias temporales. Los eventos entrelazados, como `PagoRecibido` y `EnvioIniciado`, requieren reglas claras de orden. La consistencia eventual implica que el resultado llega, pero no inmediatamente — algo difícil para equipos acostumbrados a flujos síncronos. Y la curva de aprendizaje es empinada: no es trivial ver "cómo funciona el sistema" cuando todo está desacoplado. Por eso se recomienda partir el problema en tres: dominio, contexto del evento, reglas de cada contexto. Cuándo considerar esta arquitectura: cuando la reacción a algo que pasó es más importante que el flujo directo, cuando necesitas auditoría completa del estado, cuando múltiples sistemas necesitan reaccionar al mismo hecho, o cuando la escalabilidad independiente es crítica. La pregunta no es "¿cuándo llegó el evento?" sino "¿qué debe pasar cuando llegue?".

---

## SLIDE 13 — Arquitectura limpia (Clean Architecture)

**Título:** Círculos concéntricos. Dependencias hacia adentro

**La idea central:**
- Organizar el código en **círculos concéntricos**.
- Cada círculo tiene su propia responsabilidad.
- El código del centro **no sabe que existe el exterior**.

**Los 4 círculos (de adentro hacia afuera):**

**C1 — Entidades (el centro):**
- Reglas de negocio a nivel de empresa.
- La lógica más pura del dominio.
- No dependen de nada externo.

**C2 — Casos de uso:**
- Lógica de negocio de la aplicación.
- Orquestan las entidades para cumplir un objetivo.
- Dependen de las entidades, pero no de nada exterior.

**C3 — Adaptadores de interfaz:**
- Controladores, presenters, gateways.
- Su única responsabilidad: **transferir datos** entre el exterior y el interior.
- No tienen lógica de negocio.

**C4 — Frameworks y drivers (afuera):**
- Base de datos, frameworks web (Django, FastAPI, Express).
- Interfaces de usuario.
- Dispositivos externos.
- **La base de datos es un detalle**.

**Regla de dependencia:**
> *Las dependencias apuntan hacia adentro, nunca hacia afuera.*

**Errores comunes:**
- La base de datos no valida los casos de uso.
- El modelo de BD no es la entidad.
- Depender 100% de un framework es un error.

**Por qué importa:**
- Cambiar de base de datos sin tocar la lógica de negocio.
- Cambiar de framework web sin tocar los casos de uso.
- Testear la lógica de negocio sin BD ni UI.
- Entender el código sabiendo siempre en qué círculo estás.

**Guion extendido para el orador:**

La arquitectura limpia, propuesta originalmente por Robert C. Martin (Uncle Bob), es una de las formas más elegantes de organizar código. La idea central es muy visual: organizas tu código en círculos concéntricos, como las capas de una cebolla. Cada círculo tiene su propia responsabilidad, y el código del centro no sabe que existe el exterior. Esa es la regla de oro: **las dependencias apuntan hacia adentro, nunca hacia afuera**. El círculo más interno es el de las entidades. Aquí viven las reglas de negocio puras del dominio, la lógica más importante de tu sistema. Una entidad `Pedido`, por ejemplo, sabe validar que no se puede confirmar un pedido sin al menos un item. Esa regla vive aquí, en el centro, y no depende de absolutamente nada externo. No sabe que existe una base de datos, no sabe que existe un framework web, no sabe que existe un usuario. Solo sabe las reglas del negocio. El siguiente círculo es el de los casos de uso. Aquí vive la lógica de la aplicación: cómo se orquestan las entidades para cumplir un objetivo. El caso de uso `ConfirmarPedido`, por ejemplo, usa la entidad `Pedido` para validar, y luego dispara los efectos necesarios. Los casos de uso dependen de las entidades, pero no de nada exterior. Después vienen los adaptadores de interfaz: los controladores que reciben requests HTTP, los presenters que formatean las respuestas, los gateways que son interfaces para acceder a datos externos. Su única responsabilidad es transferir datos entre el mundo exterior y el interior. No tienen lógica de negocio. Finalmente, en el círculo más externo, están los frameworks y drivers: la base de datos, el framework web que uses (Django, FastAPI, Express), las interfaces de usuario, los dispositivos externos. Todo esto son detalles. Intercambiables. La base de datos es un detalle: podrías cambiar de MySQL a PostgreSQL y el resto del sistema no se enteraría. ¿Por qué funciona esta separación? Porque te da libertad. Puedes cambiar de framework web sin tocar la lógica de negocio. Puedes testear la lógica sin necesidad de base de datos ni interfaz de usuario. Puedes entender el código sabiendo siempre en qué círculo estás parado. Los errores más comunes al implementar arquitectura limpia son: creer que la base de datos valida los casos de uso (no, las reglas viven en entidades y casos de uso); confundir el modelo de base de datos con la entidad (son cosas distintas — la entidad tiene lógica, el modelo de BD solo persiste); y depender al 100% de un framework, lo que te deja atrapado. Los datos sí cruzan los círculos, pero la lógica no. Cuando llega un request, el controlador lo recibe, lo convierte al formato del dominio, llama al caso de uso, el caso de uso aplica la lógica con las entidades, devuelve el resultado, y el controlador lo convierte de vuelta al formato externo. Los datos transfieren. La lógica solo existe hacia adentro.

---

## SLIDE 14 — Principios SOLID (parte 1)

**Título:** SOLID: las 5 reglas del diseño orientado a objetos

**S — Responsabilidad Única (SRP):**
- *Una clase debe tener una sola razón para cambiar.*
- Si una clase tiene dos o más actores que pueden pedirle cosas distintas, ya tiene dos razones para cambiar.

**O — Abierto/Cerrado (OCP):**
- *Abierta a expansión, cerrada a modificación.*
- Cuando necesitas nueva funcionalidad, extiendes por herencia, no modificas la clase existente.

**L — Sustitución de Liskov (LSP):**
- *Las subclases deben poder sustituir a la clase padre sin romper nada.*
- El clásico problema del pingüino que no puede volar.

**Guion extendido para el orador:**

SOLID es un acrónimo que reúne cinco principios de diseño orientado a objetos que, aplicados correctamente, producen código más mantenible, más flexible y más fácil de cambiar. Fueron popularizados por Robert C. Martin y se han convertido en una de las bases del diseño profesional de software. Vamos a ver los tres primeros en esta slide y los dos restantes en la siguiente. El primer principio es el de Responsabilidad Única, o SRP por sus siglas en inglés. La idea es simple: una clase debe tener una sola razón para cambiar. ¿Qué significa eso en la práctica? Que si una clase tiene dos o más actores que pueden pedirle cosas distintas, ya tiene dos razones para cambiar. Imagina una clase `ProcesarPedido` que tiene tres métodos: `calcular_precio`, `asignar_ruta` y `generar_factura`. El equipo de Ventas quiere cambiar cómo se calculan los precios. El equipo de Envíos quiere cambiar la lógica de rutas. El equipo de Finanzas quiere cambiar la facturación. Esa clase tiene tres razones para cambiar, y eso es una violación directa del SRP. La solución es separar en tres clases distintas: `ServicioPrecios`, `ServicioEnvios`, `ServicioFacturacion`, cada una con una sola razón de cambio. El segundo principio es Abierto/Cerrado, o OCP. La regla dice: una clase debe estar abierta a expansión, pero cerrada a modificación. ¿Qué significa eso? Que cuando necesitas agregar nueva funcionalidad, no modificas la clase existente: la extiendes por herencia. Un ejemplo clásico es una calculadora. Si tienes una clase `Calculadora` con un método `multiplicar` y un método `dividir`, y mañana necesitas agregar `restar`, lo correcto no es modificar la clase `Calculadora` para agregarle el método. Lo correcto es crear una clase base abstracta `Calculadora` con un método abstracto `operar`, y luego tener subclases `Sumar`, `Restar`, `Multiplicar`, `Dividir`. Agregar una nueva operación es crear una nueva clase, no tocar la base. Esto te protege de romper funcionalidades existentes cuando agregas nuevas. El tercer principio es el de Sustitución de Liskov, o LSP. Este dice que las subclases deben poder sustituir a la clase padre sin romper nada. El ejemplo clásico es el de los pájaros. Tienes una clase padre `Pajaro` con un método `volar()`. Tienes una subclase `Pinguino` que hereda de `Pajaro`. Pero el pingüino no puede volar. ¿Qué haces? Si fuerzas al `Pinguino` a implementar `volar()` lanzando una excepción, has roto el principio de Liskov: ya no puedes usar un `Pinguino` donde esperabas un `Pajaro` sin que falle. La solución es usar composición por interfaces: defines interfaces pequeñas como `IFly` (volar), `ISwim` (nadar), `IEat` (comer), y cada pájaro implementa solo las que necesita. El `Loro` implementa `IFly` y `IEat`. El `Pinguino` implementa `ISwim` y `IEat`. El `Pato` implementa las tres. Cualquiera puede usarse donde corresponde sin romper nada. Si pasamos a la siguiente slide, vemos los dos principios restantes.

---

## SLIDE 15 — Principios SOLID (parte 2)

**Título:** SOLID: las 5 reglas del diseño orientado a objetos (continuación)

**I — Segregación de Interfaces (ISP):**
- *Prefiere muchas interfaces pequeñas por acción, sobre una mega-interfaz con todo.*

**D — Inversión de Dependencia (DIP):**
- *Depende de abstracciones, no de implementaciones concretas.*

**Tabla resumen:**

| Letra | Principio | Idea |
|---|---|---|
| S | Responsabilidad Única | Una clase, una razón para cambiar |
| O | Abierto/Cerrado | Expansión por herencia, no modificación |
| L | Sustitución de Liskov | Subclases sustituyen al padre sin romper |
| I | Segregación de Interfaces | Interfaces pequeñas, no mega |
| D | Inversión de Dependencia | Abstracciones, no implementaciones |

**Frase importante:**
> *"Estos principios no son reglas absolutas — son guías. El objetivo es código fácil de cambiar, no código que cumpla todos los principios en papel."*

**Guion extendido para el orador:**

Continuamos con los dos últimos principios SOLID. El cuarto es el de Segregación de Interfaces, o ISP. La regla dice: prefiere muchas interfaces pequeñas por acción, sobre una mega-interfaz con todo. La idea es que ninguna clase debe verse forzada a implementar métodos que no va a usar. Imagina una interfaz `IAnimal` que tiene tres métodos abstractos: `volar()`, `nadar()` y `caminar()`. Ahora quieres crear una clase `Perro`. El perro no vuela, no nada (en general), pero camina. Con la mega-interfaz, el `Perro` tiene que implementar `volar()` y `nadar()` aunque no los necesite, simplemente porque la interfaz los declara. Eso es una violación de ISP. La solución es segregar: defines `IVolador` con `volar()`, `INadador` con `nadar()`, `ICaminante` con `caminar()`. El `Perro` implementa `ICaminante` y `INadador`, nada más. El `Gato` implementa solo `ICaminante`. El `Pato` implementa las tres. Cada clase implementa solo lo que necesita, sin métodos vacíos ni innecesarios. Y el quinto principio, y último, es el de Inversión de Dependencia, o DIP. Este es probablemente el más importante de los cinco. La regla dice: depende de abstracciones, no de implementaciones concretas. Los módulos de alto nivel no deben depender de módulos de bajo nivel; ambos deben depender de abstracciones. Un ejemplo clásico: tienes una clase `Interruptor` y una clase `Bombilla`. El `Interruptor` está conectado directamente a la `Bombilla`. ¿Qué pasa si mañana quieres conectar el mismo interruptor a un `Ventilador` o a una `Lampara`? Tienes que modificar la clase `Interruptor`. Eso es un acoplamiento alto. La solución es introducir una abstracción: defines una interfaz `Dispositivo` con un método `encender()`. La `Bombilla`, el `Ventilador` y la `Lampara` implementan `Dispositivo`. El `Interruptor` ahora depende de `Dispositivo`, no de `Bombilla` directamente. Cuando construyes un `Interruptor`, le pasas el dispositivo por inyección de dependencias. Puedes conectar un ventilador, una bombilla o una lámpara, y el `Interruptor` no cambia nunca. Para agregar un nuevo dispositivo, solo creas una nueva clase que implementa `Dispositivo`. Y aquí va una aclaración importante: SOLID no son reglas absolutas. Son guías. Aplicarlas dogmáticamente, por cumplir la regla sin entender el contexto, lleva a sobreingeniería. El objetivo no es tener código que cumpla SOLID en un paper. El objetivo es tener código que sea fácil de cambiar, fácil de testear, fácil de entender. A veces una clase con dos responsabilidades es perfectamente válida. A veces una mega-interfaz es la mejor opción. Lo importante es entender el principio detrás de la regla, y aplicarlo cuando aporta valor real.

---

## SLIDE 16 — Cuándo usar un patrón de diseño

**Título:** Primero el problema. Después el patrón.

**El error más común:**
- Buscar un patrón primero y luego intentar encajar el problema dentro de él.
- El orden correcto es:
  1. Entiendes bien el problema.
  2. Entiendes bien el dominio.
  3. El dominio define qué patrón necesitas, no al revés.

**El patrón no simplifica el problema — lo estructura:**
- Si tu dominio es complejo, el patrón que uses también lo será.

**No siempre necesitas un patrón:**
- Si el problema es simple y una función lo resuelve, déjalo simple.

**Puedes mezclar patrones:**
- Strategy + Observer + Repository + Factory en un mismo proyecto es válido.

**Pasos antes de aplicar cualquier patrón:**
1. Entender el problema.
2. Conocer el dominio.
3. Buscar el patrón correcto.
4. Entender la forma canónica.
5. Evaluar si es realmente necesario.

**Frase para recordar:**
> *"El patrón no crea la solución — el dominio la define y el patrón la estructura."*

**Guion extendido para el orador:**

Uno de los errores más comunes en el desarrollo de software, especialmente en developers con poca experiencia, es enamorarse de los patrones de diseño y empezar a aplicarlos en todos lados. "Voy a usar Factory aquí. Acá necesito un Observer. Esto pide un Singleton a gritos". Y se termina con código lleno de patrones que nadie entiende, que resuelven problemas que no existen, y que hacen que el sistema sea mucho más complejo de lo necesario. ¿Cuándo usar un patrón? La respuesta corta: cuando el problema lo pide, no cuando tu ego lo pide. El error más común es buscar un patrón primero y luego intentar encajar el problema dentro de él. El orden correcto es al revés. Primero entiendes bien el problema. Después entiendes bien el dominio. Y solo entonces el dominio te dice qué patrón necesitas. El patrón no simplifica el problema. Eso es clave. Un patrón estructura, organiza, le da una forma canónica. Pero si tu dominio es complejo, el patrón que uses para resolverlo también será complejo. No hay forma de ocultar la complejidad del negocio detrás de un patrón elegante. La expectativa correcta es que el patrón te da una forma canónica de organizar el código, ayuda a que otros developers lo entiendan rápido, y no reduce la complejidad del negocio, solo la hace manejable. Antes de aplicar un patrón, necesitas entender cómo se aplica correctamente. Un patrón tiene una forma canónica, una estructura probada que resuelve el problema específico. Si no entiendes esa forma antes de implementar, puedes aplicar el patrón incorrectamente, crear una versión que no resuelve nada, o añadir complejidad sin beneficio. Un consejo práctico: si no puedes explicar el problema con tus propias palabras sin mencionar el patrón, aún no estás listo para usarlo. Y no siempre necesitas un patrón. Si el problema es simple y una función lo resuelve, déjalo simple. Un solo archivo con lógica directa es más claro que un patrón "por moda". El código simple y directo siempre es mejor que el código "patronizado" que nadie entiende. Eso sí, puedes mezclar patrones en un mismo proyecto. Un proyecto puede usar varios patrones simultáneamente: Strategy para tipos de pago, Observer para notificar cambios, Repository para acceder a datos, Factory para crear instancias. Cada patrón resuelve un problema específico. No necesitas elegir uno solo. Y no reinventes la rueda. Los patrones existen porque desarrolladores han atacado los mismos problemas una y otra vez. Si existe un patrón que resuelve tu problema, úsalo. No importa si el patrón tiene 50 años. Si se adapta a tu problema, úsalo. MVC lleva décadas y sigue siendo válido. Repository Pattern es antiguo y resuelve muy bien el acceso a datos. CQRS es más nuevo, pero no es la solución para todo. La pregunta no es "¿es moderno?", es "¿me resuelve el problema?". El principio más importante: conoce bien tu problema antes de buscarle un patrón. El patrón no crea la solución, el dominio la define y el patrón la estructura.

---

## SLIDE 17 — Costos, trade-offs y lenguaje común

**Título:** La gestión estructural define los costos

**Tipos de empresa por gestión estructural:**

| Tipo | Estrategia | Prioridad |
|---|---|---|
| Exploratoria | Busca su nicho | Expandir, aprender, encontrar product-market fit |
| Con nicho establecido | Ya conoce su mercado | Invertir en mejorar y eficiencia |
| Ahorro primero | Prioriza reducir costos | Costos antes que nuevas funciones |

**La pregunta clave: ¿por qué ganamos dinero?**
- ¿Por qué el cliente nos elige?
- ¿Tenemos ventaja competitiva?
- ¿Disponibilidad, precio, alguna insignia (ISO)?

**Trade-offs y costo de oportunidad:**
- Alta disponibilidad → mayor costo de infraestructura.
- Alta escalabilidad → mayor complejidad.
- Tiempo de entrega rápido → posiblemente menor calidad.
- El arquitecto debe hacer **explícitos** estos balances, no ocultarlos.

**Lenguaje del dominio del negocio:**
- El arquitecto debe **crear el lenguaje** para que todos entiendan.
- Si no lo hace, se cae en el **efecto Babel**: todos buscan el mismo objetivo pero hablan idiomas diferentes.

**Matriz de traducción técnico → negocio:**

| Técnico | Negocio | Significa |
|---|---|---|
| Latencia | Tiempo de respuesta | Cuánto tarda el sistema |
| Throughput | Capacidad de atención | Cuántos usuarios simultáneos soporta |
| Failover | Continuidad operativa | Qué pasa si un servidor se cae |
| Deuda técnica | Mantenimiento pendiente | Trabajo que retrasa nuevas funciones |
| SLA | Nivel de servicio prometido | Qué compromiso tenemos con el cliente |
| Escalabilidad horizontal | Crecer sin mejorar hardware | Más servidores vs. servidor más grande |
| Consistencia eventual | Puede tardar en actualizarse | Datos no sincronizados al instante |
| ACID | Transacción segura | Si falla algo, se revierte todo |

**Frase para recordar:**
> *"El arquitecto no solo diseña sistemas — diseña comunicación que permite que el sistema exista."*

**Guion extendido para el orador:**

Esta slide es una de las más importantes para alguien que quiere aplicar arquitectura de software en una empresa real. Vamos a hablar de dinero, de comunicación y de cómo las decisiones técnicas afectan al negocio. Empecemos por la gestión estructural. Toda empresa tiene una forma de organizarse, y esa forma define qué costos importan. Una empresa exploratoria, que está buscando su nicho de mercado, va a priorizar expandir, aprender, encontrar el product-market fit. El costo que más le importa es el costo de oportunidad: ¿qué pasa si invierto en esto y el mercado cambia? Una empresa con nicho establecido, que ya sabe a quién le vende, va a invertir en mejorar y ser más eficiente. Y una empresa de ahorro primero, que ya tiene su mercado y solo quiere reducir costos, va a priorizar eso por encima de nuevas funciones. Dependiendo del tipo, los costos significan cosas distintas. No se optimiza igual en una startup que en una empresa de ahorro. Y aquí viene la pregunta clave: ¿por qué ganamos dinero? ¿Por qué el cliente nos elige a nosotros? ¿Tenemos ventaja competitiva? ¿Disponibilidad? ¿Precio? ¿Tenemos alguna insignia, como una certificación ISO, que el cliente esté buscando? Las respuestas a estas preguntas determinan qué costos importan y qué se optimiza primero. Si tu ventaja competitiva es la disponibilidad, entonces tu prioridad de inversión es alta disponibilidad, aunque cueste más en infraestructura. Si tu ventaja es el precio, entonces tu prioridad es reducir costos operativos. Ahora hablemos de trade-offs. Cada decisión arquitectónica tiene un costo de oportunidad. La palabra en chino "权衡" (zhèng huái) significa "sopesar, balancear", y es perfecta para esto. Si haces A, no haces B. Si inviertes en alta disponibilidad, gastas más en infraestructura. Si buscas alta escalabilidad, aumentas la complejidad operativa. Si quieres entregar rápido, posiblemente sacrificas calidad. El arquitecto debe hacer explícitos estos balances, no ocultarlos. Decir "hagamos esto porque sí" sin hablar de los trade-offs es irresponsable. El equipo y el negocio necesitan entender qué están ganando y qué están sacrificando. Y aquí viene uno de los roles más importantes del arquitecto: crear un lenguaje común. ¿Por qué? Porque en cualquier empresa, tarde o temprano, surge el efecto Babel: todos buscan el mismo objetivo, pero hablan idiomas diferentes. El equipo técnico habla de latencia, throughput, consistencia eventual. El equipo de negocio habla de tiempo de respuesta, capacidad de atención, datos no sincronizados al instante. Si el arquitecto no diseña y facilita esta comunicación, la solución no funciona. Por eso existe la matriz de traducción técnico-negocio. Es una herramienta simple pero poderosa. Una tabla que dice: "cuando yo digo latencia, lo que el negocio escucha es tiempo de respuesta". Esta matriz vive en la documentación del proyecto y se comparte con todo el mundo: el equipo de desarrollo, los stakeholders de negocio, los product managers. Un ejemplo práctico: si dices "tenemos problemas de consistencia eventual en la base de datos", el negocio te mira con cara de confusión. Pero si dices "el usuario puede ver precios antiguos por unos segundos después de un cambio", todos entienden. Y eso es lo que permite tomar decisiones informadas. El arquitecto no solo diseña sistemas, diseña comunicación que permite que el sistema exista.

---

## SLIDE 18 — Malas prácticas que debes evitar

**Título:** Las 5 trampas más comunes en arquitectura

**1. Ilusión de productividad:**
- Entregar mucho, pero con baja calidad no aceptable para producción.

**2. Dependencia de un proveedor (vendor lock-in):**
- Evitar depender de un agente o servicio externo — o estarás atrapado a sus reglas.

**3. Résumé driven development:**
- Priorizar logros personales en resultados del equipo y producto.

**4. Parálisis por análisis:**
- Los developers no empiezan porque el arquitecto no ha tomado decisiones.

**5. Sistemas infinitamente personalizables:**
- Intentar ir más allá y solucionar problemas que no se presentan aún.

**Guion extendido para el orador:**

Estas son las cinco trampas más comunes en arquitectura de software. Las he visto una y otra vez en proyectos reales, y conocerlas es la mejor forma de evitarlas. La primera es la ilusión de productividad. Es muy fácil caer en esta trampa: el equipo entrega muchas features, el product owner está contento porque ve avance, los managers ven gráficas de burndown que se mueven hacia abajo. Pero la calidad de lo entregado es baja. El código "funciona" en el sentido de que pasa los tests, pero no tolera el uso real. Tiene bugs latentes, deuda técnica acumulada, problemas de seguridad no resueltos. Es como construir una casa rápido: se ve bien por fuera, pero las paredes están huecas. La métrica que se está midiendo es la cantidad de features entregadas, no el valor real generado. Y cuando llega el día de producción, todo se cae. La segunda trampa es la dependencia de un proveedor. Esto es lo que se conoce como vendor lock-in. A veces es imposible evitarlo: usas un servicio cloud, una API externa, una librería de un solo mantenedor. Pero la pregunta es: ¿qué pasa si ese proveedor cambia sus precios, descontinúa el servicio, o quiebra? ¿Qué tan atrapado estás? Si la respuesta es "mucho", tienes un problema serio. Sin proveedor tienes libertad; con proveedor tienes que negociar poder de negociación, y a veces no lo tienes. La tercera trampa es el résumé driven development, y esta es particularmente insidiosa. Sucede cuando las decisiones técnicas se toman pensando en el currículum, no en el problema. "Vamos a usar Kubernetes porque queda bien en el CV. Vamos a meter microservicios aunque tengamos tres usuarios. Vamos a usar blockchain para un sistema de inventarios de cinco productos". El resultado es un stack que brilla en presentaciones pero complica el mantenimiento, aumenta los costos y no resuelve mejor el problema. La cuarta trampa es la parálisis por análisis. Esta es más sutil. El arquitecto quiere tomar la decisión perfecta, considera todas las alternativas, espera tener toda la información antes de actuar. Mientras tanto, el equipo está bloqueado, esperando el OK del arquitecto para empezar a trabajar. El diseño perfecto nunca llega, pero el proyecto se estanca. Hay que saber cuándo el diseño está "suficientemente bien" y tomar la decisión. Se puede iterar después. Y la quinta trampa es construir sistemas infinitamente personalizables. Esto es la sobreingeniería pura. "Qué pasa si el usuario quiere hacer X" — se construye para X aunque nadie lo pida. "Algún día podríamos necesitar Y" — se agregan abstracciones que no resuelven nada actual. El resultado es un sistema tan complejo que nadie lo entiende, tan genérico que no resuelve bien nada concreto, y tan caro de mantener que mata al proyecto. La regla es simple: construye para lo que necesitas hoy, con la flexibilidad de cambiar mañana. Eso es madurez arquitectónica.

---

## SLIDE 19 — Fitness Functions: cómo evitar las malas prácticas

**Título:** Pruebas que verifican que la arquitectura cumple sus objetivos

**¿Qué son?**
- Pruebas que verifican que la arquitectura cumple con sus objetivos de diseño.

**Tipos de fitness functions:**

**Métricas:**
- Validar con datos que todo va según los objetivos de diseño.

**Pruebas unitarias en código:**
- Validar que el código cumple con las decisiones tomadas y es funcional.

**Ingeniería del caos:**
- Ir a golpear al servidor a ver si sobrevive.
- Inundar la red, apagar partes, provocar fallos controlados.
- Netflix Chaos Monkey es el ejemplo clásico.

**Monitoreo:**
- Darle seguimiento a todo lo que se hace en producción.
- Métricas, logs, alertas, dashboards.

**Frase para recordar:**
> *"Sin fitness functions, tu arquitectura es solo un documento que nadie verifica."*

**Guion extendido para el orador:**

¿Cómo evitamos caer en las malas prácticas que acabamos de ver? La respuesta está en las fitness functions. Este concepto, introducido por Neal Ford y otros autores de la comunidad de arquitectura evolutiva, se refiere a pruebas que verifican que la arquitectura cumple con sus objetivos de diseño. Es decir, son mecanismos objetivos para saber si tu arquitectura sigue viva o si se está pudriendo. Hay varios tipos. Las métricas te permiten validar con datos que todo va según los objetivos. Por ejemplo, si tu objetivo era que el sistema respondiera en menos de 200ms, tienes una métrica que mide eso en producción. Si en algún momento la métrica sube a 800ms, sabes que algo se rompió arquitectónicamente. Las pruebas unitarias en código validan que el código cumple con las decisiones tomadas. Si decidiste que los casos de uso no pueden depender de la base de datos, escribes una prueba que verifica que efectivamente no hay esa dependencia. Esas pruebas son tu red de seguridad. La ingeniería del caos es fascinante y un poco terrifying al principio. La idea es literalmente ir a golpear al servidor a ver si sobrevive. Apagas instancias aleatoriamente, inundas la red con tráfico, simulas latencia, provocas fallos controlados. Si el sistema sobrevive, sabes que es resiliente. Si se cae, sabes exactamente qué falla. Netflix popularizó esto con su herramienta Chaos Monkey, que apaga instancias de producción de forma aleatoria. Suena loco, pero les ha permitido construir uno de los sistemas más resilientes del mundo. Y finalmente, el monitoreo. Métricas, logs, alertas, dashboards. Darle seguimiento a todo lo que se hace en producción. El monitoreo no es solo para encontrar bugs: es para verificar que las decisiones arquitectónicas siguen siendo válidas a lo largo del tiempo. Las cuatro tipos de fitness functions son complementarias. Las métricas y los tests unitarios te dan feedback temprano, en desarrollo. La ingeniería del caos te da confianza sobre la resiliencia. El monitoreo te da visibilidad continua en producción. Sin fitness functions, tu arquitectura es solo un documento que nadie verifica. Y un documento que nadie verifica es solo ficción.

---

## SLIDE 20 — Ley de Conway y comunicación

**Título:** Los sistemas reflejan la organización

**Ley de Conway:**
> *"Los sistemas generados reflejan la comunicación interna de la organización."*

**Cómo se manifiesta:**
- Si la empresa tiene silos → la arquitectura termina en silos.
- Si hay colaboración interdisciplinaria → los equipos cruzan fronteras.
- Si la comunicación es jerárquica → las decisiones fluyen de arriba hacia abajo.

**Patrones comunes de organización:**

*Estructura jerárquica o centralizada:* decisiones de arriba hacia abajo.

*Estructura matricial:* colaboración interdisciplinaria.

*Equipos aislados (silos):* dificultan la comunicación efectiva.

*Comunidades de práctica:* redes informales de intercambio de conocimiento.

**Comunicación con el equipo:**
- Documentos sobre plantillas alineadas con la cultura de la organización.
- Evitar el "está bien" sin feedback real.
- Incentivar preguntas y objeciones.

**Técnicas útiles:**
- **Cinco por qué**: iterar preguntando "por qué" cinco veces.
- **Seis sombreros**: considerar múltiples perspectivas.

**Guion extendido para el orador:**

La Ley de Conway es una de esas observaciones simples pero profundas que cambian cómo ves los sistemas. Melvin Conway la formuló en los años 60, y dice: "los sistemas generados reflejan la comunicación interna de la organización". Esto significa que la forma en que tu empresa se comunica determina, en gran medida, la forma que tendrá tu software. Si tu empresa tiene silos — equipos que no se hablan, departamentos aislados, información que no fluye — tu arquitectura va a terminar teniendo silos. Van a aparecer módulos que se comunican mal, dependencias rotas, integraciones que nadie mantiene. Si en tu empresa hay colaboración interdisciplinaria, si devs, diseño, producto y operaciones trabajan juntos desde el inicio, tu arquitectura va a reflejar eso: equipos que cruzan fronteras, sistemas que se integran limpiamente, decisiones que se toman en conjunto. Si la comunicación es jerárquica, con decisiones que fluyen de arriba hacia abajo, tu arquitectura va a ser jerárquica: capas estrictas, aprobaciones formales, cambios lentos. La Ley de Conway no es una opinión del arquitecto. Es un diagnóstico. Cuando llegas a una empresa nueva, mira la estructura de comunicación y te va a contar la historia de la arquitectura. Por eso el arquitecto debe identificar el estilo de comunicación de la empresa y usarlo en sus documentos. No es suficiente con hacer un buen diseño técnico: el diseño tiene que encajar en cómo la gente realmente trabaja. Hay varios patrones comunes de organización. La estructura jerárquica o centralizada tiene toma de decisiones que fluye desde arriba. Es común en empresas grandes y en el sector público. Tiene ventajas en estabilidad, pero es lenta para innovar. La estructura matricial promueve la colaboración interdisciplinaria. Es típica de empresas de tecnología maduras. Los equipos aislados en silos dificultan la comunicación efectiva y generan los problemas arquitectónicos que mencionamos. Las comunidades de práctica son redes informales de intercambio de conocimiento, donde gente de distintos equipos comparte experiencias y buenas prácticas. Son muy valiosas para la innovación. La comunicación con el equipo es clave. Las reuniones deben mostrar documentos construidos sobre plantillas, no presentaciones improvisadas. Hay que evitar el "está bien" sin feedback real. Hay que incentivar preguntas y objeciones. Y hay dos técnicas muy útiles que vale la pena mencionar. Los "cinco por qué" es una técnica de Toyota: cuando tienes un problema, preguntas "por qué" cinco veces seguidas para llegar a la causa raíz. Los "seis sombreros para pensar" es de Edward de Bono: consideras el problema desde seis perspectivas distintas — datos, emociones, crítica, optimismo, creatividad, overview — para tener una visión completa.

---

## SLIDE 21 — Serendipia: el oro inesperado del buen diseño

**Título:** El mejor diseño resuelve problemas que no sabías que tenías

**El equipo y la auto-capacitación:**
- Un equipo no debe estar amarrado a hacer las cosas de una sola forma.
- La tecnología está en constante cambio — todo sistema debe estar preparado para actualizarse.

**Qué es la serendipia en arquitectura:**
- Un diseño bien pensado **abre la puerta a resolver problemas laterales** que aún no existían como prioridades.

**Cómo cultivar la serendipia:**
- **Espacio para experimentación**: prototipos sin la presión de "esto va a producción".
- **No forzar innovación**: la serendipia real surge cuando no se busca a propósito.
- **Ver el diseño desde múltiples ángulos**: interno y externo.

**AI como espejo del diseño:**
- ¿Qué se podría mejorar?
- ¿Hay puntos que no se cubren?
- ¿Qué podría fallar?
- ¿Qué herramientas existentes podrían ayudarme con esto?

**Feedback como herramienta:**
- Del equipo de desarrollo.
- De los usuarios.
- De la AI como interlocutor crítico.
- Del monitoreo en producción.

**Frase para recordar:**
> *"La serendipia no es suerte — es el resultado de diseñar con intención y luego tener la apertura de notar lo que surgió sin haberlo planeado."*

**Guion extendido para el orador:**

Quiero cerrar la parte teórica de esta sesión hablando de algo que no se ve en los libros de arquitectura, pero que es fundamental: la serendipia. La serendipia es encontrar oro sin buscarlo. Es cuando tu diseño, bien pensado, termina resolviendo un problema que ni siquiera sabías que ibas a tener. Suena a suerte, pero no lo es. La serendipia es el resultado de diseñar con intención y luego tener la apertura de notar lo que surgió sin haberlo planeado. Para cultivar la serendipia en un equipo, hay tres ingredientes. El primero es el espacio para experimentación. Un equipo necesita tiempo y permiso para hacer prototipos sin la presión de que tienen que ir a producción. Esos prototipos, aunque no se lancen, generan aprendizaje, generan ideas, y a veces generan esos descubrimientos laterales que terminan siendo oro puro. El segundo ingrediente es no forzar la innovación. La innovación real no surge cuando se impone, surge cuando se permite. Las famosas "horas de innovación" de Google (el 20% time) funcionan bien para features nuevas, pero la serendipia más profunda surge de manera orgánica, sin que nadie la esté buscando activamente. El tercer ingrediente es ver el diseño desde múltiples ángulos. No solo desde el interno — cómo se construye, cómo se mantiene — sino también desde el externo: cómo se usa, cómo se siente el usuario, cómo podría evolucionar. Una herramienta poderosa para esto, en el mundo actual, es la inteligencia artificial. La AI nos puede ayudar a ver nuestro propio diseño con ojos críticos. Le puedes pedir que se haga preguntas incómodas: ¿qué se podría mejorar? ¿Hay puntos que no se cubren? ¿Qué podría fallar? ¿Qué herramientas existentes podrían ayudarme con esto? Estas preguntas obligan a stressear el diseño antes de que el código lo demuestre en producción. La AI no reemplaza al arquitecto, pero es un excelente interlocutor crítico. Y finalmente, el feedback es la herramienta que convierte un diseño estático en uno que evoluciona. Feedback del equipo de desarrollo, de los usuarios, de la AI como interlocutor crítico, del monitoreo en producción. Sin feedback, la arquitectura se queda congelada en el momento en que se creó. Con feedback, se convierte en un documento vivo. El mejor diseño es aquel que resuelve problemas que no sabías que tenías. Esa es la esencia de la serendipia aplicada a la arquitectura.

---

## SLIDE 22 — Cómo aplicar estos fundamentos en la empresa real

**Título:** De la teoría al impacto: cómo mejorar tu empresa con pensamiento arquitectónico

**Esta es la sección nueva que conecta todo lo anterior con la práctica empresarial.**

### 1. Reducir costos de codificación con buenas prácticas de diseño

**El problema:**
- Código mal organizado cuesta más de mantener que de escribir.
- Se estima que entre el 60% y el 80% del tiempo de un developer se va en mantener código existente, no en escribir código nuevo.
- Si tu código es un monolito sin módulos, con responsabilidades mezcladas, dependencias circulares y sin tests, ese costo se multiplica.

**Cómo lo resuelven los fundamentos:**
- **SRP (Responsabilidad Única)**: clases con una sola responsabilidad son más fáciles de entender, modificar y testear. Menos tiempo perdido en "qué hace este código".
- **OCP (Abierto/Cerrado)**: agregar funcionalidades sin modificar código existente reduce el riesgo de regresiones.
- **Arquitectura limpia**: separar entidades, casos de uso y adaptadores permite cambiar de framework o de base de datos sin reescribir la lógica de negocio. Migraciones que antes costaban meses, ahora cuestan semanas.
- **Principios SOLID en general**: código que cumple SOLID es más fácil de refactorizar, lo que reduce el costo de evolución del sistema.

**Beneficio empresarial concreto:**
- Reducción del 30-50% en tiempo de desarrollo de nuevas features (dato de la industria).
- Menor tiempo de onboarding para nuevos developers.
- Menos bugs en producción.
- Mayor velocidad de entrega al mercado.

### 2. Mejorar procesos de la empresa con visión arquitectónica

**El problema:**
- Los procesos de la empresa (cómo se aprueba un cambio, cómo se priorizan features, cómo se hace deploy) están íntimamente ligados a la arquitectura.
- Procesos rígidos + arquitectura monolítica = innovación lenta.
- Procesos caóticos + microservicios = caos multiplicado.

**Cómo lo resuelven los fundamentos:**
- **Documentación de decisiones (ADR)**: cada decisión técnica importante queda registrada, con su contexto, alternativas consideradas y consecuencias. Esto acelera las reuniones, evita debates recurrentes y permite que cualquier persona del equipo entienda el "por qué" de las decisiones pasadas.
- **Fitness functions**: las métricas, tests de arquitectura, ingeniería del caos y monitoreo se convierten en parte del proceso de release. Ya no es "deploy and pray", es "deploy con confianza porque las fitness functions nos dicen que estamos bien".
- **Comunicación estructurada**: usar plantillas para documentos de arquitectura, técnicas como los cinco porqués y los seis sombreros, y comunidades de práctica, mejora la calidad de las decisiones y reduce el tiempo de las reuniones.
- **Matriz de traducción técnico-negocio**: alinea al equipo técnico con stakeholders de negocio. Las decisiones de arquitectura se toman con información completa, no con suposiciones.

**Beneficio empresarial concreto:**
- Reuniones un 40% más cortas y productivas.
- Decisiones técnicas con menos retrabajo.
- Mejor alineación entre negocio y tecnología.
- Procesos que escalan con el equipo, no que se rompen al crecer.

### 3. Tomar decisiones de tecnología con impacto en costos

**El problema:**
- Elegir mal una tecnología puede costar meses de migración y cientos de miles de dólares.
- Elegir bien puede ahorrar años de trabajo y permitir enfocarse en lo que genera valor.

**Cómo lo resuelven los fundamentos:**
- **Contexto primero**: antes de elegir tecnología, entender el tipo de empresa, su estrategia y su equipo. Esto evita sobre-invertir en startups y sub-invertir en empresas establecidas.
- **Trade-offs explícitos**: cada decisión arquitectónica viene con su balance. Documentar los trade-offs permite que la organización entienda qué se está ganando y qué se está sacrificando.
- **Estilos de arquitectura progresivos**: empezar con monolito modular y migrar a microservicios solo cuando el problema y la madurez lo justifiquen. Esto evita el error común de pagar los costos de microservicios sin tener los beneficios.
- **Costo total de propiedad**: considerar no solo el costo de implementación, sino también el de operación, mantenimiento y personal.

**Beneficio empresarial concreto:**
- Decisiones de tecnología que escalan con el negocio.
- Menos migraciones forzadas por errores del pasado.
- Mejor ROI en infraestructura cloud.
- Menos dependencia de proveedores (vendor lock-in reducido).

### 4. Mejorar la comunicación técnica dentro de la empresa

**El problema:**
- Los developers hablan un idioma, los managers hablan otro, los stakeholders de negocio hablan otro. El efecto Babel está en todas partes.
- Esto genera retrabajo, expectativas mal alineadas y decisiones tomadas con información incompleta.

**Cómo lo resuelven los fundamentos:**
- **Matriz de traducción técnico-negocio**: herramienta concreta para alinear el lenguaje.
- **C4 Model**: diagramas por niveles (contexto, contenedores, componentes, código) que cualquier persona puede entender, no solo developers.
- **ADR**: documentos cortos y estructurados que cualquier stakeholder puede leer.
- **Comunidades de práctica**: espacios informales donde developers comparten conocimiento y buenas prácticas.

**Beneficio empresarial concreto:**
- Mejor comunicación entre equipos técnicos y de negocio.
- Menos "traducciones" y malentendidos costosos.
- Documentación que la gente realmente lee.

### 5. Escalar el equipo sin perder velocidad

**El problema:**
- Cuando el equipo crece, las decisiones se vuelven más lentas, las reuniones se multiplican, y la arquitectura se convierte en un cuello de botella.
- Esto es especialmente cierto en empresas que crecieron rápido y no adaptaron su arquitectura ni sus procesos.

**Cómo lo resuelven los fundamentos:**
- **Estilos de arquitectura modulares**: el monolito modular permite que distintos equipos trabajen en distintos módulos sin estorbarse.
- **Ley de Conway aplicada a propósito**: si rediseñas la arquitectura, rediseña la organización. Si rediseñas la organización, la arquitectura se ajustará. Hacerlo conscientemente es mejor que dejar que pase por accidente.
- **Contratos bien definidos (SOA, OpenAPI)**: permiten que distintos equipos trabajen en paralelo sobre distintos servicios, siempre que respeten los contratos.
- **Eventos como mecanismo de integración**: desacoplan equipos que solo necesitan saber "qué pasó", no "cómo pasó".

**Beneficio empresarial concreto:**
- Equipos que pueden trabajar en paralelo sin estorbarse.
- Onboarding más rápido de nuevos developers.
- Decisiones que se distribuyen, no se centralizan.
- Velocidad de entrega que se mantiene o aumenta al crecer el equipo.

### 6. Crear una cultura de mejora continua

**El problema:**
- Sin feedback continuo, la arquitectura se queda obsoleta.
- Los sistemas legacy que vemos en muchas empresas son el resultado de años sin revisar las decisiones arquitectónicas.

**Cómo lo resuelven los fundamentos:**
- **Serendipia cultivada**: dar espacio para experimentación, usar AI como espejo del diseño, abrirse a descubrir problemas laterales.
- **Feedback loops**: del equipo, de los usuarios, de la AI, del monitoreo.
- **Fitness functions vivas**: las métricas, los tests de arquitectura y la ingeniería del caos evolucionan con el sistema.
- **ADRs vivos**: cada decisión importante se registra, se revisa periódicamente y se actualiza si el contexto cambia.

**Beneficio empresarial concreto:**
- Sistemas que evolucionan con el negocio, no que se quedan atrás.
- Menos reescrituras desde cero.
- Cultura de "aprender y mejorar" en lugar de "culpar y rehacer".

### Resumen ejecutivo: el impacto empresarial de los fundamentos

| Fundamento | Impacto empresarial |
|---|---|
| Contexto y requisitos | Decisiones alineadas con el negocio |
| Cliente-servidor | Base para cualquier sistema distribuido |
| Estilos de arquitectura | Capacidad de escalar técnica y organizacionalmente |
| Monolito bien hecho | Simplicidad operativa y bajo costo |
| Microservicios con cabeza | Escalamiento cuando realmente se necesita |
| Eventos | Desacoplamiento y trazabilidad |
| Arquitectura limpia | Código mantenible y migraciones baratas |
| SOLID | Código fácil de cambiar y testear |
| Patrones con criterio | Soluciones probadas, no reinventadas |
| Costos y trade-offs | Decisiones financieras informadas |
| Malas prácticas evitadas | Menos deuda técnica y retrabajo |
| Fitness functions | Sistemas que sobreviven a producción |
| Ley de Conway | Arquitectura alineada con la organización |
| Serendipia | Descubrimientos valiosos no planeados |

**Frase para cerrar esta sección:**
> *"Estos fundamentos no solo te hacen mejor developer — te hacen mejor profesional. Te dan herramientas para reducir costos, mejorar procesos, tomar mejores decisiones y tener un impacto real en el negocio."*

**Guion extendido para el orador:**

Esta es la parte más importante de toda la presentación, porque conecta todo lo que hemos visto con la práctica empresarial real. Porque sí, los fundamentos de arquitectura de software son interesantes desde el punto de vista técnico. Pero su verdadero valor está en el impacto que generan en la empresa. Vamos por partes. Primero, reducir costos de codificación. El código mal organizado cuesta más de mantener que de escribir. La industria estima que entre el 60% y el 80% del tiempo de un developer se va en mantener código existente, no en escribir código nuevo. Si tu código es un monolito sin módulos, con responsabilidades mezcladas, dependencias circulares y sin tests, ese costo se multiplica. Los principios SOLID, la arquitectura limpia, las decisiones de estilo bien tomadas, todo eso reduce el costo de mantenimiento. Menos tiempo perdido en "qué hace este código", menos bugs en producción, mayor velocidad de entrega. Segundo, mejorar procesos. Los procesos de la empresa están íntimamente ligados a la arquitectura. Procesos rígidos con arquitectura monolítica generan innovación lenta. Procesos caóticos con microservicios generan caos multiplicado. Las herramientas de los fundamentos — ADRs, fitness functions, comunicación estructurada, matriz de traducción — se convierten en procesos que escalan con el equipo, no que se rompen al crecer. Tercero, tomar decisiones de tecnología con impacto en costos. Elegir mal una tecnología puede costar meses de migración. Elegir bien ahorra años. Los fundamentos te dan el marco para tomar esas decisiones con información completa: contexto, trade-offs, costo total de propiedad. Cuarto, mejorar la comunicación técnica. El efecto Babel está en todas partes. La matriz de traducción, el C4 Model, los ADRs, las comunidades de práctica: todo eso reduce los malentendidos costosos entre developers, managers y stakeholders. Quinto, escalar el equipo sin perder velocidad. La arquitectura modular, la Ley de Conway aplicada conscientemente, los contratos bien definidos, los eventos como mecanismo de integración: todo eso permite que equipos grandes trabajen en paralelo sin estorbarse. Y sexto, crear una cultura de mejora continua. Sin feedback continuo, la arquitectura se queda obsoleta. Los sistemas legacy que vemos en muchas empresas son el resultado de años sin revisar las decisiones. La serendipia cultivada, los feedback loops, las fitness functions vivas, los ADRs vivos: todo eso mantiene los sistemas relevantes. El mensaje final es este: estos fundamentos no solo te hacen mejor developer. Te hacen mejor profesional. Te dan herramientas para reducir costos, mejorar procesos, tomar mejores decisiones y tener un impacto real en el negocio. Y eso es lo que al final justifica todo el tiempo que invertiste en aprender arquitectura de software.

---

## SLIDE 23 — Cierre y siguientes pasos

**Título:** Lo que aprendimos hoy (y lo que sigue)

**Recap rápido:**
1. La arquitectura es una **responsabilidad**, no un título.
2. El **contexto** define la solución — no al revés.
3. Hay 5 estilos principales: **monolito → monolito modular → microservicios → eventos**.
4. La **arquitectura limpia** organiza el código en círculos concéntricos.
5. **SOLID** son 5 principios para mantener el código mantenible.
6. Los **patrones** resuelven problemas canónicos — pero el problema va primero.
7. **Costos, trade-offs y lenguaje común** son tan importantes como la tecnología.
8. Las **fitness functions** verifican que la arquitectura sigue viva.
9. La **Ley de Conway** dice que la organización modela al sistema.
10. La **serendipia** aparece cuando diseñas con intención y apertura.
11. **Todo esto se traduce en impacto empresarial real**: menos costos, mejores procesos, mejores decisiones.

**Siguientes pasos sugeridos para el estudiante:**
- Practicar identificando el estilo de arquitectura de 3 aplicaciones que uses a diario.
- Leer un ADR de un proyecto open source y tratar de replicarlo.
- Dibujar la arquitectura de un sistema pequeño que conozcas usando el modelo C4.
- Intentar refactorizar un módulo siguiendo los principios SOLID y ver qué pasa.
- Experimentar con un broker de eventos (Kafka, RabbitMQ) en un proyecto pequeño.
- Identificar una mala práctica en tu equipo actual y proponer una solución basada en los fundamentos.

**Frase final:**
> *"No existe el estilo perfecto. Existe el estilo que tu organización puede operar hoy sin convertirse en caos."*

---

## ANEXO — Prompt sugerido para herramienta de IA

Si vas a usar una herramienta de IA generativa de presentaciones (Gamma, Beautiful.ai, SlidesAI, etc.), te sugiero este prompt base, ya ajustado a este material:

```
Crea una presentación de 23 diapositivas titulada "Fundamentos de
Arquitectura de Software", con tono didáctico, en español, dirigida
a estudiantes de programación o developers que quieren profesionalizar
su forma de pensar el software.

Duración objetivo: 60-90 minutos (presentación completa).

Estilo visual: limpio, profesional, con paleta neutra y acentos en
azul/verde. Tipografía sans-serif. Diagramas minimalistas cuando
hagan falta (círculos concéntricos para Clean Architecture, líneas
de tiempo para la progresión de estilos, tablas comparativas para
los estilos arquitectónicos).

Estructura: 1 portada + 1 índice + 21 diapositivas de contenido +
1 slide de cierre. El contenido exacto de cada slide está en el
siguiente bloque. Genera primero el outline y luego las slides:

[PEGA AQUÍ EL CONTENIDO DE LAS SLIDES 1 A 23 DE ESTE DOCUMENTO]

Reglas:
- Cada slide debe tener un título claro y máximo 5-7 bullets.
- Si un bullet es muy largo, divídelo en dos líneas.
- Resalta las frases para recordar en negrita o en un bloque
  destacado.
- Incluye una slide final con 5 preguntas de repaso para la
  audiencia.
- La slide 22 (Cómo aplicar estos fundamentos en la empresa real)
  es la más importante: dedica tiempo extra a diseñarla bien, con
  visuales que muestren el impacto empresarial.
```

**Tip:** Si la herramienta que usas no soporta pegar todo de una vez, ve copiando bloque por bloque (`SLIDE 1`, `SLIDE 2`, etc.) y pídele que genere cada slide por separado. Eso te da más control sobre el resultado final.

---

*Documento generado a partir de las notas del repositorio `Learning/arquitectura-software/` (David, 2026), con sección adicional sobre aplicación empresarial.*
