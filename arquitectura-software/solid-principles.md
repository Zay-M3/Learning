# Los 5 Principios SOLID

> Principios de diseño orientado a objetos para crear código más mantenible y flexible.

---

## 1. SRP — Responsabilidad Única (Single Responsibility Principle)

**Una clase debe tener una sola razón para cambiar.**

Si una clase tiene dos o más actores que pueden pedirle cosas distintas, ya tiene dos razones para cambiar. Eso viola el principio.

### Ejemplo

```python
# ❌ VIOLA SRP — múltiples razones para cambiar
class ProcesarPedido:
    """Equipo de Ventas quiere cambiar precios,
       Equipo de Envíos quiere cambiar lógica de destino,
       Equipo de Finanzas quiere cambiar facturación."""

    def calcular_precio(self): ...
    def asignar_ruta(self): ...
    def generar_factura(self): ...
    # Esta clase tiene TRES razones para cambiar
```

```python
# ✅ CUMPLE SRP — una razón de cambio por clase
class ServicioPrecios:
    """Solo Equipo de Ventas"""
    def calcular_precio(self): ...

class ServicioEnvios:
    """Solo Equipo de Envíos"""
    def asignar_ruta(self): ...

class ServicioFacturacion:
    """Solo Equipo de Finanzas"""
    def generar_factura(self): ...
```

---

## 2. OCP — Abierto/Cerrado (Open/Closed Principle)

**Una clase debe estar abierta a expansión, pero cerrada a modificación.**

Cuando necesitas agregar nueva funcionalidad, no modificas la clase existente — la extiendes por herencia.

### Ejemplo

```python
# ❌ VIOLA OCP — modificas la clase cada vez que agregas operación
class Calculadora:
    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        return a / b

    # Si agregas restar, modificas Calculadora original ← viola OCP
```

```python
# ✅ CUMPLE OCP — extiendes por herencia, no modificas la original
from abc import ABC, abstractmethod

class Calculadora(ABC):
    """Clase base — NUNCA se modifica"""
    @abstractmethod
    def operar(self, a, b):
        pass

class Multiplicar(Calculadora):
    def operar(self, a, b):
        return a * b

class Dividir(Calculadora):
    def operar(self, a, b):
        return a / b

class Restar(Calculadora):
    def operar(self, a, b):
        return a - b

class Sumar(Calculadora):
    def operar(self, a, b):
        return a + b

# Agregar nueva operación = crear nueva clase, nunca tocar Calculadora
```

---

## 3. LSP — Sustitución de Liskov (Liskov Substitution Principle)

**Las subclases deben poder sustituir a la clase padre sin romper nada.**

Si tienes una clase padre `Pajaro`, cualquier subclase debe poder usarse en su lugar sin comportamientos inesperados. El clásico problema del pingüino que no puede volar.

### Ejemplo

```python
# ❌ VIOLA LSP — Pingüino fuerza implementar volar() pero no puede
class Pajaro:
    def volar(self):
        print("Volando")
    def comer(self):
        print("Comiendo")

class Pinguino(Pajaro):
    def volar(self):
        raise Exception("No puedo volar")  # ← rompe LSP
```

```python
# ✅ CUMPLE LSP — composición por interfaces
from abc import ABC, abstractmethod

class IFly(ABC):
    @abstractmethod
    def volar(self): pass

class ISwim(ABC):
    @abstractmethod
    def nadar(self): pass

class IEat(ABC):
    @abstractmethod
    def comer(self): pass

class Loro(IEat, IFly):
    def comer(self): print("Loro comiendo")
    def volar(self): print("Loro volando")

class Pinguino(IEat, ISwim):
    def comer(self): print("Pinguino comiendo")
    def nadar(self): print("Pinguino nadando")
    # No tiene IFly — perfectamente válido

class Pato(IEat, IFly, ISwim):
    def comer(self): print("Pato comiendo")
    def volar(self): print("Pato volando")
    def nadar(self): print("Pato nadando")

# Cualquiera puede usarse donde corresponda sin romper nada
def hacer_volar(obj: IFly):
    obj.volar()

hacer_volar(Loro())   # ✓
hacer_volar(Pato())   # ✓
# hacer_volar(Pinguino())  # ← TypeError en tiempo de creación, no en runtime
```

---

## 4. ISP — Segregación de Interfaces (Interface Segregation Principle)

**Prefiere muchas interfaces pequeñas por acción, sobre una mega-interfaz con todo.**

Ninguna clase debe verse forzada a implementar métodos que no va a usar.

### Ejemplo

```python
# ❌ VIOLA ISP — mega-interfaz, las clases heredan lo que no necesitan
class IAnimal(ABC):
    @abstractmethod
    def volar(self): pass
    @abstractmethod
    def nadar(self): pass
    @abstractmethod
    def caminar(self): pass

class Perro(IAnimal):
    def volar(self): pass      # no necesita pero debe implementar
    def nadar(self): pass      # no necesita pero debe implementar
    def caminar(self): print("Perro caminando")  # sí necesita
```

```python
# ✅ CUMPLE ISP — interfaces separadas por acción
class IVolador(ABC):
    @abstractmethod
    def volar(self): pass

class INadador(ABC):
    @abstractmethod
    def nadar(self): pass

class ICaminante(ABC):
    @abstractmethod
    def caminar(self): pass

class Perro(ICaminante, INadador):
    def caminar(self): print("Perro caminando")
    def nadar(self): print("Perro nadando")
    # No hereda IVolador — no necesita volar

class Gato(ICaminante):
    def caminar(self): print("Gato caminando")
    # Solo lo que necesita

class Pato(ICaminante, INadador, IVolador):
    def caminar(self): print("Pato caminando")
    def nadar(self): print("Pato nadando")
    def volar(self): print("Pato volando")
```

---

## 5. DIP — Inversión de Dependencia (Dependency Inversion Principle)

**Depende de abstracciones, no de implementaciones concretas.**

Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.

### Ejemplo

```python
# ❌ VIOLA DIP — Interruptor depende directamente de Bombilla
class Bombilla:
    def encender(self):
        print("Bombilla encendida")

class Interruptor:
    def __init__(self):
        self.bombilla = Bombilla()  # ← alto acoplamiento

    def presionar(self):
        self.bombilla.encender()

# Si quieres conectar un Ventilador → tienes que cambiar Interruptor
```

```python
# ✅ CUMPLE DIP — Interruptor depende de abstracción
from abc import ABC, abstractmethod

class Dispositivo(ABC):
    """Abstracción — contrato que define el comportamiento"""
    @abstractmethod
    def encender(self): pass

class Bombilla(Dispositivo):
    def encender(self):
        print("Bombilla encendida")

class Ventilador(Dispositivo):
    def encender(self):
        print("Ventilador encendido")

class Lampara(Dispositivo):
    def encender(self):
        print("Lampara encendida")

class Interruptor:
    """Depende de la abstracción, no de lo concreto"""
    def __init__(self, dispositivo: Dispositivo):  # ← inyección de dependencia
        self.dispositivo = dispositivo

    def presionar(self):
        self.dispositivo.encender()

# Uso
interruptor_bombilla = Interruptor(Bombilla())
interruptor_bombilla.presionar()  # Bombilla encendida

interruptor_ventilador = Interruptor(Ventilador())
interruptor_ventilador.presionar()  # Ventilador encendido

# Para un nuevo dispositivo → solo creas la clase, Interruptor no cambia
interruptor_lampara = Interruptor(Lampara())
```

---

## Resumen

| # | Principio | Qué dice |
|---|---|---|
| **S** | Responsabilidad Única | Una clase, una razón para cambiar |
| **O** | Abierto/Cerrado | Abierto a expansión, cerrado a modificación |
| **L** | Sustitución de Liskov | Las subclases deben sustituir a la clase padre sin romper |
| **I** | Segregación de Interfaces | Interfaces pequeñas por acción, no mega-interfaces |
| **D** | Inversión de Dependencia | Depender de abstracciones, no de implementaciones concretas |

---

## Nota

Estos principios no son reglas absolutas — son guías. Aplicarlos dogmáticamente puede llevar a sobreingeniería. El objetivo es código que sea fácil de cambiar, no código que cumpla todos los principios en papel.