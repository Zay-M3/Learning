# Ejemplos de Extraccion de Requisitos por Dominio

Ejercicios practicos para aprender a sacar requisitos reales de situaciones comunes.

---

## Caso 1: Agente de atencion al cliente (tu caso)

### El problema inicial
El cliente dice: "Quiero un chatbot para WhatsApp que responda preguntas de clientes."

### Aplicando los 5 Porques
- Por que quiere un chatbot? Para responder mas rapido
- Por que responder mas rapido? Porque los clientes se van si esperan mucho
- Por que se van? Porque tenemos 3 personas atendiendo y no alcanzan
- Por que solo 3? Porque no hay presupuesto para mas personal
- Por que no hay presupuesto? Porque las ventas se han reducido

**Problema real:** Las ventas se redujeron por falta de atencion. El chatbot es la solucion — pero el verdadero objetivo es recuperar ventas.

### Requisito funcional derivado
El agente debe responder en menos de 30 segundos en horario laboral. Si el agente no puede resolver la consulta, debe escalar a humano en menos de 5 minutos.

### Requisito no funcional derivado
El sistema debe manejar 50 consultas simultaneas sin degradar el tiempo de respuesta.

### De aqui sale la historia de usuario
Como cliente
quiero resolver mi duda por WhatsApp en menos de 30 segundos
para no tener que esperar ni llamar por telefono

---

## Caso 2: Sistema de inventario para una muebleria

### El problema inicial
El cliente dice: "Quiero controlar mi inventario."

### Observando el trabajo actual
El-dueno de la muebleria te muestra su proceso:
- Todo en cuadernos
- Cuando alguien pregunta "tengo este sofa en existencia?" tiene que buscar 20 minutos
- A veces vende algo que ya no tiene y tiene que disculparse con el cliente

### El flujo actual vs deseado

**Actual:**
```
[Cliente pregunta por sofa modelo Roma] 
→ El dueno busca en 3 cuadernos 
→ 20 minutos 
→ A veces dice "creo que si" y resulta que no
→ Cliente furioso
```

**Deseado:**
```
[Cliente pregunta por sofa modelo Roma]
→ El dueno busca en el sistema en 3 segundos
→ Inmediato dice si o no con la cantidad exacta
→ Si no hay, muestra alternativas en existencia
```

### Requisitos funcionales derivados
1. Registrar productos con: nombre, modelo, categoria, cantidad, precio
2. Buscar productos por nombre o modelo
3. Alerta automatica cuando la cantidad baja de 5 unidades
4. Historial de movimientos de entrada y salida

### Requisitos no funcionales derivados
1. El sistema debe funcionar offline en tienda (la conexion es inestable)
2. Deben poder usar tablet y celular
3. Los datos se sincronizan cuando hay conexion

---

## Caso 3: Software para restaurant pequeno

### El problema inicial
El dueo dice: "Quiero una app para tomar pedidos."

### La observation revela
El restaurant tiene 8 mesas. El problema principal no es la toma de pedidos — es que se confunden de pedido entre cocina y mesero. El plato sale a la mesa equivocada 4-5 veces por semana.

### La diferencia entre querer y necesitar

| Lo que dice | Lo que significa |
|---|---|
| "Quiero una app para pedidos" | Cree que el problema es la toma de pedidos |
| El problema real | La comunicacion entre mesero y cocina es deficiente |
| Solucion correcta | Una pizarra digital en cocina + notificacion cuando cambia un pedido |

### La historia correcta
Como cocinero
quiero ver inmediatamente cuando un pedido cambia o se cancela
para no cocinar algo que ya no se necesita

---

## Caso 4: Dashboard de ventas para empresa de servicios

### El problema inicial
El gerente dice: "Necesito un dashboard con graficos de ventas."

### Los 5 Porques
- Por que quiere graficos? Para ver como vamos este mes
- Por que necesita verlo? Porque no sabe si va bien o mal hasta que recibe estados financieros
- Por que no lo sabe antes? Porque los datos se consolidan manualmente cada fin de mes
- Por que se consolidan manualmente? Porque cada vendedor lleva sus datos en Excel separado
- Por que en Excel separado? Porque no hay un sistema central

**Problema real:** Los vendedores no reportan en tiempo real. El dashboard es util solo si los datos entran en tiempo real.

### Requisito funcional clave
Cada vendedor debe poder registrar su venta en el sistema en maximo 5 minutos despues de cerrar el trato.

### Requisito no funcional
El dashboard debe actualizarse en tiempo real conforme los vendedores registran ventas.

---

## Ejercicio para practicar

Piensa en tu propio trabajo o un negocio que conozcas bien. Aplica los 4 principios:

1. Cual es el objetivo de negocio (aumentar, reducir, mitigar)?
2. Escribe 3 terminos del negocio y su traduccion tecnica (glosario)
3. Cuales serian 2 requisitos no funcionales importantes?
4. Dibuja en Excalidraw el flujo actual y el flujo deseado

Esto te entrena a pensar como ingeniero de requisitos.

---

## Siguiente paso

Ver: priorizacion-de-requisitos.md para aprender como decidir que requisitos hacer primero.