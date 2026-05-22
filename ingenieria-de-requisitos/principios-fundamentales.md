# Principios Fundamentales de Ingenieria de Requisitos

## Principio 1: El objetivo del negocio

Un requerimiento solo es valido si cumple al menos uno de estos tres objetivos:

- **Aumentar ganancias** — el sistema genera mas ingresos
- **Reducir costos** — el sistema abarata operaciones existentes
- **Mitigar riesgo** — el sistema evita perdidas futuras

Si un requerimiento no cae en ninguna de estas tres categorias, es ruido y debe archivarse o guardarse para despues.

> Si no esta generando dinero, ahorrando dinero, o evitando que se pierda dinero, la inversion en ese requerimiento no se justifica.

### Ejemplo: Agente de IA para incidencias

Un chatbot que responde preguntas basicas de clientes no vende directamente ni reduce personal. Pero mitiga el riesgo de fuga de clientes — alguien que pregunta y no recibe respuesta en 2 horas se va con la competencia.

Eso es un requerimiento valido por mitigacion de riesgo.

---

## Principio 2: Hablar en el idioma del dominio

El ingeniero de requisitos es un traductor. No habla en tecnico — habla como el negocio.

Un buen requerimiento es aquel que el cliente puede leer y entender sin saber nada de software.

### El glosario compartido

Cada proyecto debe tener un glosario que traduje lenguaje de negocio a tecnico:

| Termino de negocio | Significado tecnico |
|---|---|
| Orden de pedido | Entidad Order en la DB, con estado, cliente, items |
| Confirmar pedido | Cambio de estado pending → confirmed |
| El pedido se cae | Estado payment_failed o cancelled |
| Activar producto | Toggle is_active=True en la tabla producto |

### El punto ciego

El desarrollador asume que entiende el negocio cuando en realidad no. Cada dominio tiene matices que solo se descubren preguntando, no asumiendo.

> Si hay algo que el cliente usa y yo desconozco, pregunto. No asumo. El glosario se construye entre ambos.

---

## Principio 3: Los requisitos no funcionales son requisitos

Un requisito no funcional mal detectado es mucho mas costoso de incorporar una vez el sistema esta en produccion.

Un requisito no funcional como el rendimiento o la concurrencia puede afectar directamente si el objetivo del negocio se cumple o se pierde.

### Categorias de requisitos no funcionales

| Categoria | Pregunta clave | Ejemplo |
|---|---|---|
| **Desempeno** | Cuanto tiempo es aceptable? | Respuesta en menos de 3 segundos |
| **Escalabilidad** | Cuantos usuarios simultaneos? | 500 usuarios simultaneos |
| **Seguridad** | Que datos protege? | Datos de clientes encriptados |
| **Disponibilidad** | Cuanto uptime necesita? | 99.5% mensual |
| **Tecnologia** | Hay restricciones de stack? | Solo PostgreSQL |
| **Despliegue** | Donde se ejecuta? | AWS con fallback on-prem |
| **Compatibilidad** | Que dispositivos? | Chrome, Firefox, Safari — ultimos 2 anos |
| **Regulatorio** | Normas legales? | Datos de clientes en Colombia (Ley 1581) |

### Preguntas no funcionales esenciales

- Cuantos pedidos simultaneos manejan hoy? Y en 2 anos?
- Hay algun requerimiento legal sobre donde se almacenan los datos?
- El sistema necesita estar disponible 24/7 o puede tener ventanas de mantenimiento?
- Cuantos usuarios van a usar el sistema concurrentemente?
- Que pasa si el sistema se cae a media manana?

### Error comun

Pensar que los no funcionales se detectan en pruebas o despues de produccion. Se detectan en la primera reunion de requisitos.

---

## Principio 4: Nunca ir a una reunion sin un prototipo

Ir a una reunion con el cliente sin algo tangible genera incertidumbre. El cliente no sabe si el desarrollador le entiende.

El prototipo dice: - No es codigo de produccion - No tiene que funcionar de verdad - Solo tiene que verse como la solucion y permitir interaccion basica - Se construye en horas, se desecha despues

### Por que funciona el prototipo

1. El cliente valida con sus ojos, no con su imaginacion. Ah,