# Historias de Usuario

Formatos y buenas practicas para escribir historias de usuario que el equipo y el cliente entiendan.

## Formato basico

Como [tipo de usuario]
quiero [accion]
para [beneficio/valor]

## Ejemplos por dominio

### E-commerce / Ventas

Como vendedor
quiero ver la lista de productos mas vendidos del mes
para identificar que reabastecer y que promover

---

Dado que el inventario tiene menos de 10 unidades
cuando un cliente agrega ese producto al carrito
entonces mostrar alerta de stock bajo y sugerir similares

---

### Agente de atencion al cliente

Como cliente que pregunta por WhatsApp
quiero recibir respuesta en menos de 30 segundos
para no esperar y resolver rapido

---

Como agente de soporte
quiero ver el historial del cliente
para no pedir la misma informacion dos veces

---

### Sistema de inventario / Logistica

Como auxiliar de bodega
quiero registrar entrada de productos con codigo de barras
para no escribir mal las referencias

---

## Reglas de una buena historia

1. Independiente — no depende de otra historia
2. Negociable — el detalle se ajusta en conversacion
3. Valiosa — aporta valor al usuario final
4. Estimable — el equipo puede decir cuanto cuesta
5. Pequena — se completa en 1-2 dias maximo

## Criterios de aceptacion

Cada historia necesita criterios claros:

- El campo de busqueda acepta minimo 3 caracteres
- Los resultados aparecen en menos de 2 segundos
- Si no hay resultados, se muestra mensaje claro
- El historial se guarda aunque el usuario cierre la app

## Tallas

| Tamano | Tiempo | Descripcion |
|---|---|---|
| XS | 1-4 horas | Un campo, un boton |
| S | 1-2 dias | Un formulario simple |
| M | 3-5 dias | Varias pantallas |
| L | 1-2 semanas | Un modulo completo |

Si una historia es mayor a L, se divide.

## Siguiente paso

Ver: tecnicas-de-elicitacion.md