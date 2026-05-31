# Microservicios

> Dividir la aplicación en pequeños servicios independientes, cada uno con una función concreta.

---

## Fundamentos

Los microservicios consisten en **dividir la aplicación en pequeños servicios o módulos concretos**. Cada servicio es independiente de los demás y se encarga de una función específica.

A diferencia del monolito, donde todo vive en un solo proceso, cada microservicio tiene:
- Su propio proceso
- Su propia base de datos (idealmente)
- Su propio ciclo de desarrollo y deploy

Esto permite que cada servicio evolucione de forma independiente.

---

## Gestión de contratos de datos

Es fundamental establecer **contratos bien definidos y claros** para las conexiones entre servicios.

Un contrato define:
- Qué datos se intercambian
- En qué formato
- Qué operaciones están disponibles
- Qué respuestas se esperan

Cuando un contrato está bien definido, cada microservicio puede evolucionar de forma independiente **sin romper las integraciones con los otros**. Un cambio interno en un servicio no debería afectar a sus consumidores si el contrato se respeta.

---

## Costos operativos y de producción

Los costos son un factor clave — **no solo en el desarrollo inicial, sino en el costo operacional continuo**.

En producción, cada microservicio debe estar:
- Conectado en la nube o en un servidor independiente
- Monitorizado individualmente
- Desplegado de forma independiente

Esto agrega:
- **Costos de infraestructura** — cada servicio necesita su propia compute, memoria, red
- **Costos de mantenimiento** — más servicios significa más cosas que pueden fallar
- **Costo de personal calificado** — se necesita gente que sepa manejar sistemas distribuidos, redes, orquestación, contenedores

El monolito es barato de operar. Los microservicios son caros de operar. La pregunta no es "¿microservicios o no?" sino "¿puedo permitirme operarlos?".

---

## Comunicación síncrona vs. asíncrona

### Síncrona

Un servicio llama a otro y **espera la respuesta** antes de continuar. Si el servicio llamado falla, el que llama también se ve afectado.

Esto puede generar **bucles que detengan todos los servicios simultáneamente** — el clásico efecto cascada.

### Asíncrona (preferida)

La comunicación entre servicios debe ser **prioritariamente asíncrona**, por eventos o streaming.

El servicio que envía no espera respuesta inmediata. Envía el evento y continúa. El consumidor procesa cuando puede.

El uso de **buffers de eventos como Kafka** es fundamental para mantener el flujo desacoplado. Si un servicio baja, el evento se queda en el broker esperando hasta que esté disponible.

> La regla: conecta servicios de forma asíncrona siempre que sea posible. Solo usa síncrono cuando el flujo lo requiera explícitamente y el riesgo de cascada sea aceptable.

---

## Patrón CQRS

**CQRS** = Command Query Responsibility Segregation

Este patrón permite **separar las operaciones de escritura (comandos) de las de lectura (consultas)**, creando modelos separados.

### Cómo funciona

- **Command (escritura):** Cuando algo cambia, se envía un comando que modifica el estado
- **Query (lectura):** Las lecturas se hacen sobre un modelo optimizado para consultas, no para escritura

### Con bases de datos distribuidas

En microservicios, cada servicio puede tener su propia base de datos. CQRS permite:
- **Escrituras** en una base de datos transaccional (su fuente de verdad)
- **Lecturas** en proyecciones optimizadas que se actualizan asíncronamente por medio de eventos

El resultado: lecturas rápidas aunque las escrituras sean complejas.

---

## Interacción entre servicios

Un cliente puede desencadenar **múltiples llamadas hacia diferentes servicios** a través de sus contratos, manteniendo la integridad y el orden durante todo el proceso.

Esto es diferente al monolito, donde una llamada puede hacerlo todo. En microservicios:

1. El cliente envía una solicitud al API Gateway o directamente a un servicio
2. Ese servicio, si necesita datos de otros, emite eventos o hace llamadas asíncronas
3. Cada servicio responde por su cuenta
4. El resultado se coordina de forma eventual

El cliente no necesita saber cuántos servicios están detrás. Solo conoce los contratos.

---

## Nota sobre microservicios y el monolito

Los microservicios no son el objetivo — son una consecuencia.

Antes de ir a microservicios:
- ¿El dominio está lo suficientemente maduro para identificar fronteras claras?
- ¿El equipo tiene madurez operativa para manejar múltiples servicios?
- ¿La organización puede absorber el costo de infraestructura y personal?
- ¿El problema realmente requiere independencia de despliegue y escalamiento?

Si la respuesta a cualquiera de estas es "no" — considera partir de un monolito modular primero.

> Los microservicios resuelven un problema de escala organizacional y técnica. Si no tienes ese problema, el monolito es la mejor opción.