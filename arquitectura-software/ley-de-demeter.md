# Ley de Demeter (Law of Demeter)

> Habla solo con tus amigos inmediatos. No encadenes llamadas a través de objetos que no te pertenecen.

---

## Origen

Proyecto Demeter (1987), popularizado por *The Pragmatic Programmer* de Hunt y Thomas. No es una regla de SOLID, pero comparte la misma motivación: reducir el acoplamiento entre piezas de código.

---

## Qué dice

Un método `M` de un objeto `O` solo puede invocar métodos de:

1. `O` mismo
2. Los argumentos de `M`
3. Cualquier objeto creado o instanciado dentro de `M`
4. Los componentes directos de `O` (sus dependencias inyectadas)

**No puede** invocar métodos de un objeto devuelto por otra invocación. En otras palabras: no encadenes llamadas.

La versión popular es **"no hables con extraños"** (don't talk to strangers) o **"una sola llamada por línea"**.

---

## Ejemplo

```python
# VIOLA Ley de Demeter — cadena de llamadas, hablar con desconocidos
class Pedido:
    def total(self):
        return self.cliente.cuenta.banco.saldo
        # Pedido habla con cliente (bien)
        # cliente expone cuenta (ya no es amigo directo de Pedido)
        # cuenta expone banco (desconocido)
        # banco expone saldo (desconocido lejano)

# CUMPLE Ley de Demeter — Pedido solo habla con su amigo cliente
class Pedido:
    def total(self):
        return self.cliente.saldo_disponible()
        # cliente sabe cómo llegar a su banco, Pedido no necesita saberlo
```

---

## Cuándo SÍ aplicarla

- Cuando una clase está accediendo a objetos profundos que no le pertenecen
- Cuando un cambio en una clase lejana obliga a cambiar tu clase
- En código de negocio donde el modelo de objetos tiene jerarquías reales

---

## Cuándo NO aplicarla

No seas dogmático. Hay casos donde encadenar es legítimo:

- **Acceso a datos simples.** `usuario.nombre` no es hablar con un extraño, es leer un campo. La regla aplica a comportamiento, no a datos.
- **Fluent APIs.** `builder.with(a).with(b).build()` está bien, el `builder` está diseñado para encadenar.
- **Streams.** `lista.map(...).filter(...).collect()` está bien, cada llamada devuelve un objeto del mismo tipo.
- **Tests y aserciones.** `response.body.user.email` es razonable en un test.

La regla detecta abuso, no prohíbe el patrón. Si en tu cadena hay objetos con lógica compleja en el medio, es momento de pararse y refactorizar.

---

## Diferencia con el resto de SOLID

| Principio | Qué problema ataca | Cómo lo resuelve |
|---|---|---|
| **SRP** | Una clase con muchas razones para cambiar | Separar en varias clases |
| **OCP** | Modificar una clase para agregar comportamiento | Extender por herencia o composición |
| **LSP** | Subclases que rompen el contrato del padre | Diseñar jerarquías correctas |
| **ISP** | Interfaces gigantes que obligan a implementar de más | Muchas interfaces pequeñas |
| **DIP** | Depender de una implementación concreta | Depender de abstracciones |
| **LoD** | Acoplar tu clase a la estructura interna de otra | No atravesar objetos que no te pertenecen |

Ley de Demeter es la versión "diseño interno" del mismo problema que DIP ataca "entre módulos".

---

## Relación con el efecto dominó

Cuando Plazit habla de evitar el efecto dominó, donde una pieza que cae hace caer a las demás, está describiendo el problema que LoD y DIP buscan resolver desde dos ángulos:

- **LoD** evita que tu código se acople a la estructura interna de otros objetos
- **DIP** evita que tu código se acople a una implementación específica de otro módulo

Ambos buscan el mismo resultado: que un cambio en una pieza no obligue a cambiar las demás.

---

## Resumen

- Habla solo con tus amigos directos, no con extraños lejanos
- Si necesitas algo de un objeto lejano, pedíselo al amigo directo, que él sabrá cómo llegar
- No acceder a cadenas de propiedades: `a.b.c.d` es una señal de alerta
- La regla aplica a comportamiento, no a datos
- No seas dogmático, fluent APIs y streams están bien
