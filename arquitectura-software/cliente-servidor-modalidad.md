# Modalidad Cliente-Servidor

> Entender la conexión entre cliente y servidor como concepto puro — antes de añadir capas de complejidad.

---

## La conexión

Es una conexión bidireccional. Tanto el cliente puede comunicarse con el servidor, como el servidor puede enviar información al cliente.

El servidor no solo responde — también puede iniciar comunicación cuando tiene algo que entregar.

---

## Dos clases de cliente

### Cliente rico

Tiene lógica dentro. Procesa eventos localmente antes de enviar información al servidor.

**Flujo:**
1. El usuario interactúa con la interfaz
2. El cliente procesa la lógica, valida, transforma
3. El cliente envía el evento ya procesado al servidor
4. El servidor corrobora la información recibida
5. Basado en el evento, procesa y envía lo solicitado de vuelta

**Características:**
- Respuesta inmediata en la interfaz (por el procesamiento local)
- Menor carga en el servidor
- Más complejidad en el cliente
- Ejemplo clásico: aplicaciones de escritorio con lógica de negocio

### Cliente ligero

Se puede representar solo como la parte visual. Está encargado de los eventos, pero no tiene casi lógica o nada.

**Flujo:**
1. El usuario interactúa con la interfaz
2. El cliente lanza la llamada al servidor
3. Todo el procesamiento ocurre en el servidor
4. El servidor devuelve el resultado
5. El cliente solo renderiza lo que recibe

**Características:**
- Lógica de negociocentralizada en el servidor
- Cliente más simple de mantener
- Mayor latencia percibida en operaciones complejas
- Ejemplo clásico: aplicaciones web tradicionales

---

## Un ejemplo conocido: la app web clásica

1. El cliente (navegador) envía eventos al servidor
2. El servidor procesa la lógica
3. El servidor llama a la base de datos (otro servidor) de donde extrae la información
4. El servidor devuelve el resultado
5. El usuario ve todo en el cliente

Este flujo es cliente ligero por excelencia — el navegador no procesa lógica de negocio, solo renderiza.

---

## Nota

Antes de entrar en patrones modernos como SPA, SSR, micro-frontends o BFF, es importante entender estos fundamentos. Son la base sobre la que todo lo demás se construye.

> Quien entiende cliente rico y cliente ligero en su forma pura, puede entender cualquier variante moderna con menos esfuerzo.