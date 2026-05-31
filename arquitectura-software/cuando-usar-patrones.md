# Cuándo Usar un Patrón de Diseño

> Los patrones resuelven problemas ya conocidos. No es necesario recrear la rueda — es mejor usar uno y entender bien qué problema ataca canónicamente.

---

## El error más común: patrón antes del problema

El mayor error es buscar un patrón primero y luego intentar encajar el problema dentro de él.

**El orden correcto es:**

1. Entiendes bien el problema
2. Entiendes bien el dominio
3. El dominio define qué patrón necesitas, no al revés

> Primero el espacio del problema. Después el patrón que lo resuelve.

---

## El patrón se vuelve tan complicado como el dominio

Un patrón de diseño **no simplifica el problema**. Lo estructura.

Si tu dominio es complejo, el patrón que uses para resolverlo también lo será. No hay forma de ocultar la complejidad del dominio detrás de un patrón elegante.

**Expectativa correcta:**
- El patrón te da una forma **canónica** de organizar el código
- El patrón te ayuda a que otros developers lo entiendan rápidamente
- El patrón no reduce la complejidad del negocio — solo la hace manejable

---

## Ver el problema de forma canónica

Antes de aplicar un patrón, necesitas entender **cómo se aplica correctamente**.

Un patrón tiene una forma canónica — una estructura probada que resuelve el problema específico. Si no lo entiendes bien antes de implementar, puedes:

- Aplicar el patrón incorrectamente
- Crear una versión que no resuelve nada
- Añadir complejidad sin beneficio

**Consejo:** antes de implementar cualquier patrón, dibuja el problema en papel. Si no puedes explicar el problema con tus propias palabras sin mencionar el patrón, aún no estás listo para usarlo.

---

## No siempre necesitas un patrón

Si no es necesario, no lo pongas por moda o por parecer profesional.

Señales de que **no necesitas un patrón:**

- El problema es simple y una función lo resuelve
- Un solo archivo con lógica directa es más claro
- No hay casos de uso futuros que justifiquen la estructura

**El código simple y directo siempre es mejor que el código "patronizado" que nadie entiende.**

---

## Puedes mezclar patrones en un proyecto

Un proyecto puede usar varios patrones simultáneamente y eso no es un problema.

**Ejemplo:**
- Usas **Strategy** para manejar tipos de pago
- Usas **Observer** para notificar cambios de estado
- Usas **Repository** para acceder a datos
- Usas **Factory** para crear instancias

Cada patrón resuelve un problema específico. No necesitas elegir uno solo.

**Lo importante es:** entender bien qué problema resuelve cada patrón y aplicarlo donde corresponde.

---

## Los patrones resuelven problemas ya conocidos

Los patrones de diseño existen porque desarrolladores han atacado los mismos problemas una y otra vez.

**No reinventes la rueda.** Si existe un patrón que resuelve tu problema, úsalo.

Esto no es pereza — es eficiencia. El tiempo que ahorras lo inviertes en lo que realmente importa: entender tu dominio.

---

## Usa el patrón que se adapte a tu caso, sin importar la edad

No importa cuánto tiempo lleva un patrón en la industria. Si se adapta a tu problema, úsalo.

**Ejemplos:**

- **MVC** — lleva décadas, pero si tu caso es simple, úsalo
- **Event-Driven Architecture** — puede ser overkill o perfecto dependiendo del caso
- **Repository Pattern** — antiguo, pero resuelve problemas de acceso a datos muy bien
- **CQRS** — más nuevo, pero no es la solución para todo

**La pregunta no es "¿es moderno?" sino "¿me resuelve el problema?"**

---

## El principio más importante

> **Conoce bien tu problema antes de buscarle un patrón. El patrón no crea la solución — el dominio la define y el patrón la estructura.**

Pasos antes de aplicar cualquier patrón:

1. **Entender el problema** — ¿qué estás tratando de resolver exactamente?
2. **Conocer el dominio** — ¿qué reglas de negocio están involucradas?
3. **Buscar el patrón correcto** — ¿cuál resuelve este problema canónicamente?
4. **Entender la forma canónica** — ¿cómo se aplica correctamente?
5. **Evaluar si es necesario** — ¿el problema realmente necesita un patrón o es más simple?

---

## Resumen

| Punto clave | Descripción |
|---|---|
| Dominio primero | El problema define el patrón, no al revés |
| No simplifica | El patrón estructura, no reduce complejidad del dominio |
| Forma canónica | Entiende cómo se aplica correctamente antes de implementar |
| No siempre es necesario | Si es simple, no lo compliques |
| Puedes mezclar | Varios patrones en un mismo proyecto son válidos |
| No reinventar | Si existe un patrón que resuelve tu problema, úsalo |
| Sin importar la edad | Si sirve, úsalo — MVC de 50 años sigue siendo válido |