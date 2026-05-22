# Criterios de Aceptacion

Como saber exactamente cuando un requisito esta "listo" y el cliente puede decir "si, esto esta bien".

---

## La diferencia entre requisito y criterio de aceptacion

El requisito dice **QUE se necesita**.
El criterio de aceptacion dice **COMO se prueba que se cumplio**.

| Requisito | Criterio de aceptacion |
|---|---|
| El agente responde consultas de clientes | El agente responde en menos de 10 segundos |
| Los datos del cliente se protegen | Solo usuarios autenticados pueden ver datos de otros |
| El inventario se actualiza en tiempo real | Al registrar entrada, el stock aumenta en maximo 2 segundos |

El requisito te dice hacia donde vas.
El criterio te dice cuando llegaste.

---

## Reglas de un buen criterio

### 1. Verificable
Se puede probar con un si o un no, no con "mas o menos".

❌ "La interfaz debe ser intuitiva"
✅ "Un usuario nuevo puede completar una compra sin ayuda en menos de 3 minutos"

### 2. Objetivo
Dos revisores llegan al mismo resultado.

❌ "El sistema es rapido"
✅ "El tiempo de respuesta no supera los 3 segundos"

### 3. Completo
Cubre happy path y casos borde.

❌ "El login funciona con correo y contrasena"
✅ "El login funciona con email y contrasena. Si la contrasena es incorrecta, muestra error. Si el email no existe, muestra error. Si el campo esta vacio, no permite enviar."

### 4. Escrito en lenguaje de negocio
No en tecnico. El cliente debe poder leerlo y saber si se cumple.

❌ "La consulta SQL tiene subindice en la columna created_at"
✅ "Los pedidos se ordenan por fecha de creacion, del mas reciente al mas antiguo"

---

## Formatos para escribir criterios

### Formato Given-When-Then (el mas usado)

```
Dado que [contexto/estado inicial]
Cuando [el usuario hace algo]
Entonces [el sistema reacciona de esta forma]
```

**Ejemplo:**
```
Dado que el cliente tiene 3 pedidos anteriores en el sistema
Cuando solicita ver "mis pedidos"
Entonces se muestran los 3 pedidos ordenados por fecha, del mas reciente al mas antiguo
Y cada pedido muestra: numero, fecha, estado y total
```

### Formato simple

```
Cuando [accion]
entonces [resultado]
```

**Ejemplo:**
```
Cuando el usuario ingresa su correo y contrasena correctos
entonces accede a su cuenta y ve un mensaje de bienvenida
```

### Lista de verificación

```
Campo: Email
- Acepta correos validos como usuario@ejemplo.com
- Rechaza correos sin @
- Rechaza correos sin dominio
- Muestra mensaje "Correo invalido" en menos de 1 segundo

Campo: Contrasena
- Minimo 8 caracteres
- Acepta espacios? No
- Muestra los caracteres como puntos (no texto plano)
```

---

## Ejemplo completo: Agente de atencion al cliente

### Requisito
"El agente debe responder preguntas frecuentes de clientes en menos de 10 segundos."

### Criterios de aceptacion

```
1. Dado que el cliente envia "donde esta mi pedido"
   Cuando el agente procesa la consulta
   Entonces responde en menos de 10 segundos
   Y proporciona el estado actual del pedido con numero de tracking (si existe)

2. Dado que el cliente envia una consulta que el agente no puede responder
   Cuando el agente no encuentra respuesta en la base de conocimiento
   Entonces escala a humano en menos de 30 segundos
   Y el cliente recibe un mensaje confirmando que fue derivado

3. Dado que el sistema tiene 50 consultas simultaneas
   Cuando todas llegan al mismo tiempo
   Entonces el tiempo de respuesta no supera los 10 segundos para ninguna
   Y no hay mensajes perdidos o mezclados entre conversaciones

4. Dado que el cliente escribe en minusculas, mayusculas o mixto
   Cuando envia su consulta
   Entonces el agente procesa sin区分大小写
   Y responde correctamente sin importar como escribio
```

---

## Ejemplo: Sistema de inventario

### Requisito
"Registrar entrada y salida de productos con control de stock."

### Criterios de aceptacion

```
1. Cuando se registra entrada de un producto
   entonces el stock de ese producto aumenta inmediatamente
   y se guarda la fecha, hora y cantidad registrada

2. Cuando se registra salida de un producto
   entonces el stock disminuye
   y si el stock resultante es menor a 5, se muestra alerta de "stock bajo"

3. Cuando se intenta registrar salida de un producto con stock = 0
   entonces el sistema impide el registro
   y muestra mensaje: "No hay stock disponible"

4. Cuando se busca un producto por nombre parcial
   entonces se muestran todos los productos que contengan ese texto
   en menos de 1 segundo

5. Cuando el sistema no tiene conexion a internet
   entonces sigue funcionando con los datos en cache
   y al reconectar sincroniza automaticamente
```

---

## Errores comunes

### ERROR 1: Confundir requisito con criterio

```
❌ Criterio: "El sistema debe enviar correos de confirmacion"
✅ Criterio: "Cuando un pedido se confirma, se envia un correo al cliente 
             en menos de 30 segundos. El correo incluye: numero de pedido,
             lista de productos, total y direccion de entrega."

❌ Criterio: "El sistema debe ser seguro"  
✅ Criterio: "Solo usuarios autenticados pueden ver datos de otros usuarios.
             Los passwords se almacenan con bcrypt. Los tokens expiran en 24 horas."
```

### ERROR 2: Criterios vagos

```
❌ "El sistema debe responder rapido"
✅ "El sistema responde en menos de 3 segundos con 100 usuarios simultaneos"

❌ "La interfaz debe ser facil de usar"
✅ "Un usuario nuevo completa el registro en menos de 2 minutos sin ayuda"
```

### ERROR 3: Solo happy path

Siempre pensar: ¿que pasa si algo sale mal?

```
❌ Solo happy path: "El login funciona con contrasena correcta"
✅ Incluir casos borde:
   - Contrasena incorrecta → mensaje de error
   - Email no registrado → mensaje de error
   - Campo vacio → no permite enviar
   - Cuenta bloqueada → indica que hacer para desbloquear
```

---

## Quien escribe los criterios

El ingeniero de requisitos facilita, pero el cliente valida.

Flujo correcto:

1. Ingeniero escribe un borrador de criterios basado en los requisitos
2. Se revisiona con el cliente
3. Cliente dice: "si, eso es lo que quiero" o "falta que..."
4. Se ajusta
5. Ambos firman (literal o digital)

Si el cliente no puede validar los criterios, significa que el requisito no esta claro todavia.

---

## Producto Incremental y Criterios

La ventaja de tener criterios claros es que facilitan la entrega incremental:

```
Sprint 1: Criterios 1 y 2 → El cliente prueba y acepta
Sprint 2: Criterios 3 y 4 → El cliente prueba y acepta
...
```

El cliente no recibe "todo o nada" al final. Va probando y corrigiendo en el camino.

---

## Checklist para revisar tus criterios

- [ ] Se puede probar con un si o un no?
- [ ] Si dos personas lo revisan, llegarian al mismo resultado?
- [ ] El cliente puede leerlo y saber si se cumple o no?
- [ ] Incluye el caso de error, no solo el caso exitoso?
- [ ] Esta en lenguaje de negocio, no en tecnico?
- [ ] Tiene numero, accion y resultado esperado?

---

## Siguiente paso

Ver: trazabilidad-de-requisitos.md para aprender como seguir cada requisito desde que se pide hasta que se construye.