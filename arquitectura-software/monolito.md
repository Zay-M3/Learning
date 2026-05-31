# Monolito

> Un módulo, un solo contenedor donde se encuentra toda la aplicación. Instalas una vez y listo, en una sola capa.

---

## Qué es

Un monolito es un estilo de arquitectura donde toda la aplicación vive en un solo proceso. Un solo deploy.

Se podría comparar con un videojuego: instalas una vez y listo. Todo está contenido en un mismo lugar.

---

## Dentro del monolito: módulos

Esto no significa que todo tenga que estar en un solo archivo. Dentro del monolito podemos tener **módulos** que separan secciones lógicas del código — cada uno con su propia responsabilidad.

Esto nos da agilidad al momento de hacer cambios, porque el código está organizado, aunque a la hora de desplegar sigue siendo todo junto.

---

## Ventajas

- **Simples de manejar**: una sola codebase, un solo deploy
- **Fáciles de adaptarse en equipos pequeños**: no hay complejidad operacional
- **Rollback simple**: si algo falla, un solo deploy hacia atrás lo revierte todo
- **Comunicación en memoria**: las llamadas entre módulos son directas, sin red

---

## Desventajas

### "Todo a la vez o nada"

Cuando haces un cambio, todo debe desplegarse. No puedes centrarte en hacer cambios en una parte mientras lo demás sigue funcionando. Es todo a la vez o nada.

Un equipo esperando deploy mientras otro está en mitad de testing es el día a día de un monolito grande.

### Ruido entre módulos (noisy neighbor)

Imaginemos este escenario:

- Dos usuarios logeados al mismo tiempo, trabajando en módulos diferentes
- El usuario 1 hace una gran carga de trabajo en su módulo
- Esto provoca que el usuario 2 tenga problemas de rendimiento o incluso no pueda hacer algunas cosas — se ve lento e inestable

Esto pasa porque **todo está en un solo lugar**. Si la base de datos es la misma para todos los módulos y no hay límites de concurrencia por recurso, un módulo puede agotar los connections pool y afectar a todos los demás.

> La modularidad dentro del monolito ayuda a nivel de código, pero si la base de datos es un monolito también, el problema persiste.

### Cuanto más crece, más duele

Cada nueva funcionalidad añade más código al mismo proceso. Los tiempos de inicio se alargan, los tests se vuelven más lentos, y la coordinación entre equipos que tocan el mismo código se complica.

---

## Cuándo considerar un monolito

- Equipos pequeños
- Problemas bien entendidos y estables
- Necesidad de simplicidad operativa
- Cuando la organización aún no tiene madurez para operar sistemas distribuidos

---

## Nota

El monolito bien hecho — con módulos claros y fronteras definidas — es el热身amiento perfecto para cuando llegue el momento de escalar a microservicios. Las fronteras que defines dentro del monolito son las mismas que vas a necesitar después.

> No es malo partir de un monolito. Es malo quedarse en un monolito sin módulos cuando el dominio ya pide separación.