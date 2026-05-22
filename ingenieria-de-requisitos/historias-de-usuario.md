# Historias de Usuario

Formatos y buenas practicas para escribir historias de usuario que el equipo y el cliente entiendan.

## Formato basico



Opcionalmente se puede agregar:



## Ejemplos por dominio

### E-commerce / Ventas

**Como** vendedor
**Quiero** ver la lista de productos mas vendidos del mes
**Para** identificar que reabastecer y que promover

---

**Dado que** el inventario tiene menos de 10 unidades de un producto
**Cuando** un cliente intenta agregar ese producto al carrito
**Entonces** mostrar una alerta de "stock bajo" y sugerir productos similares

---

### Agente de atencion al cliente (tu caso)

**Como** cliente que hace una pregunta por WhatsApp
**Quiero** recibir respuesta en menos de 30 segundos
**Para** no esperar y resolver mi problema rapido

---

**Como** agente de soporte
**Quiero** ver el historial de conversaciones del cliente
**Para** no pedir la misma informacion dos veces

---

### Sistema de inventario / Logistica

**Como** auxiliar de bodega
**Quiero** registrar la entrada de productos con codigo de barras
**Para** no escribir mal las referencias y mantener el inventario actualizado

---

## Reglas de una buena historia de usuario

1. **Independendiente** — no depende de otra historia para ser implementada
2. **Negociable** — el detalle se ajusta en conversacion con el equipo
3. **Valiosa** — aporta valor real al usuario final, no solo al tecnico
4. **Estimable** — el equipo puede decir cuanto cuesta en tiempo
5. **Pequena** — se puede completar en 1-2 dias maximo

## Criterios de aceptacion

Cada historia necesita criterios de aceptacion claros:



Los criterios de aceptacion deben ser:
- **Verificables** — se puede probar si se cumplen o no
- **Objetivos** — no hay espacio para interpretacion
- **Completos** — cubren el happy path y los casos borde

## Errores comunes

**ERROR:** "El sistema debe ser rapido"
**CORRECCION:** "El sistema debe responder en menos de 3 segundos con hasta 500 usuarios simultaneos"

---

**ERROR:** "Como usuario quiero un dashboard"
**CORRECCION:** "Como gerente de ventas quiero ver las ventas del mes por region para identificar que zonas necesitan atencion"

---

**ERROR:** "El sistema debe ser seguro"
**CORRECCION:** "Solo usuarios autenticados pueden ver datos de otros usuarios. Los passwords se almacenan con bcrypt. No hay logs que expongan tokens de sesion."

## Tallas (Sprints / Iteraciones)

| Tamano | Tiempo estimado | Descripcion |
|---|---|---|
| **XS** | 1-4 horas | Un campo, un boton, un texto |
| **S** | 1-2 dias | Un formulario simple, una validacion |
| **M** | 3-5 dias | Varias pantallas interconectadas |
| **L** | 1-2 semanas | Un modulo completo con sus casos borde |
| **XL** | 3-4 semanas | Requiere separarse en varias historias |

Si una historia es mayor a L, sedivide en historias mas pequenas.

## Siguiente paso

Ver: tecnicas-de-elicitacion.md para aprender como extraer las historias reales del cliente.