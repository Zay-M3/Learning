# Arquitectura Limpia (Clean Architecture)

> Código organizado en círculos concéntricos. Las dependencias apuntan hacia adentro, nunca hacia afuera.

---

## La idea central

La arquitectura limpia propone organizar el código en **círculos concéntricos**. Cada círculo tiene su propia responsabilidad y el código del centro no sabe que existe el exterior.

**El principio fundamental:** todo depende hacia adentro. El interior no sabe que existe el exterior.

```
┌─────────────────────────────────────────┐
│  C4: Frameworks/Drivers                 │
│  Base de datos, UI, frameworks externos  │
│  ┌─────────────────────────────────────┐│
│  │ C3: Adaptadores de interfaz          ││
│  │ Controladores, presenters, gateways ││
│  │ ┌───────────────────────────────────┐││
│  │ │ C2: Casos de uso                  │││
│  │ │ Lógica de la aplicación           │││
│  │ │ ┌─────────────────────────────────┐│││
│  │ │ │ C1: Entidades                  ││││
│  │ │ │ Reglas de negocio del dominio  ││││
│  │ │ └─────────────────────────────────┘│││
│  │ └───────────────────────────────────┘││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

---

## Los cuatro círculos

### C1 — Entidades (adentro, el centro)

Las **entidades** son el círculo más interno. Contienen:
- Las reglas de negocio a nivel de empresa
- La lógica más pura del dominio
- No dependen de nada externo

**Ejemplo:** una entidad `Pedido` sabe validar que no se puede confirmar sin al menos un item. Esa regla vive aquí.

### C2 — Casos de uso

Los **casos de uso** contienen:
- La lógica de negocio de la aplicación
- Orquestan las entidades para cumplir un objetivo
- Dependen de las entidades, pero no de nada exterior

**Ejemplo:** el caso de uso `ConfirmarPedido` usa la entidad `Pedido` para validar y confirmar.

### C3 — Adaptadores de interfaz

Los **adaptadores** contienen:
- Controladores — reciben requests y delegan
- Presenters — formatean respuestas
- Gateways — interfaces para acceder a datos externos

Su única responsabilidad: **transferir datos** entre el mundo exterior y el interior. No tienen lógica de negocio.

### C4 — Frameworks y drivers (afuera)

Vive todo lo que es detalle de implementación:
- Base de datos
- Frameworks web (Django, FastAPI, Express...)
- Interfaces de usuario
- Dispositivos externos

La base de datos es un **detalle**. Podrías cambiar de MySQL a PostgreSQL y el resto del sistema no debería enterarse.

---

## Reglas de dependencia

**Las dependencias apuntan hacia adentro, nunca hacia afuera.**

- La entidad NO sabe que existe un controlador
- El caso de uso NO sabe que existe una base de datos
- El adaptador NO sabe qué caso de uso está llamando

Si necesitas algo del círculo exterior, usas una **interfaz** (abstracción) y el círculo interior la define. Así se invierte la dependencia.

---

## Errores comunes

### La base de datos no valida los casos de uso

Las reglas de validación viven en las **entidades y casos de uso**, no en la base de datos. La BD solo persiste.

### El modelo de BD no es la entidad

Este es un error frecuente:

```
❌ WRONG: Tu modelo DB User { id, name, email, created_at, updated_at }
         y tu entidad User { id, name, email } — son lo mismo

✅ CORRECTO: Tu entidad Persona { nombre, email } + reglas de negocio
             Tu modelo User { id, email, created_at, updated_at } — solo sabe persistir
```

La entidad tiene **lógica de negocio**. El modelo de BD solo sabe **persistir**. No son lo mismo.

### Depender 100% de un framework es un error

Si toda tu lógica vive en los controllers de Django o en los handlers de FastAPI, estás atado al framework. La lógica de negocio debe poder existir **sin** el framework.

---

## Los datos cruzan círculos, no la lógica

Cuando un request llega:

1. El **controlador** recibe los datos (del círculo exterior)
2. El **controlador** los convierte a un formato del dominio y llama al caso de uso
3. El **caso de uso** aplica la lógica usando entidades
4. El **caso de uso** devuelve un resultado
5. El **controlador** convierte el resultado y lo devuelve

Los datos **transfieren**. La **lógica** solo existe hacia adentro.

---

## Por qué importa

La arquitectura limpia permite:

- **Cambiar de base de datos** sin tocar la lógica de negocio
- **Cambiar de framework web** sin tocar los casos de uso
- **Testear la lógica de negocio** sin necesidad de base de datos ni UI
- **Entender el código** sabiendo siempre en qué círculo estás

---

## Resumen

| Círculo | Qué contiene | Regla |
|---|---|---|
| Entidades | Reglas de negocio puras del dominio | No depende de nada externo |
| Casos de uso | Lógica de aplicación, orquesta entidades | Solo depende de entidades |
| Adaptadores | Controladores, presenters, gateways | Transfieren datos, no lógica |
| Frameworks/Drivers | BD, UI, frameworks | Son detalles, intercambiables |

> Lo más importante: las dependencias apuntan hacia adentro. El centro no sabe que existe el exterior.