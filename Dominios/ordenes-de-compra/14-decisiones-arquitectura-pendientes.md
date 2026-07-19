---
session: ordenes-de-compra
title: "Decisiones de arquitectura pendientes"
---

# 14 · Decisiones de arquitectura pendientes

> **Las 8 decisiones críticas que hay que tomar ANTES de implementar.** Cada una impacta significativamente el diseño técnico.

**Creado:** Julio 2026

---

## 🎯 Por qué este documento

Estas decisiones **no se pueden tomar durante la implementación** sin generar refactors caros. Hay que resolverlas ANTES de escribir código.

Cada decisión incluye:
- Contexto (por qué importa)
- Opciones (qué se puede elegir)
- Recomendación (mi sugerencia basada en tu caso)
- Impacto si se cambia después (cuánto cuesta revertir)

---

## Decisión 1: Método de valoración

### Contexto

Ya cubierto en [06 · Métodos de valoración](./06-metodos-valoracion-inventario.md). Hay que confirmar antes de codear.

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **WAC (Weighted Average Cost)** | Simple, multi-proveedor OK, España compliance | Trazabilidad lote baja |
| **FIFO** | Trazabilidad alta, España compliance | Más complejo, lot tracking |
| **LIFO** | Realidad económica en inflación | ❌ NO permitido en España (IFRS) |
| **Standard Cost** | Bueno para manufactura con presupuesto | Requiere PPV accounting complejo |

### Recomendación

✅ **WAC (Moving Average)** — por las razones del [06](./06-metodos-valoracion-inventario.md).

### Impacto si se cambia después

🔴 **ALTO.** Cambiar el método de valoración requiere migrar todos los SLEs históricos y recalcular el WAC de todo el stock. NO hacerlo en producción con stock existente.

---

## Decisión 2: Estrategia de actualización de stock

### Contexto

Ya cubierto en [05 · Estrategias de actualización de stock](./05-estrategias-actualizacion-stock.md).

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **Update on Receipt** | Simple | Precio inexacto hasta invoice |
| **Update on Invoice** | Precio exacto siempre | Stock invisible hasta invoice |
| **Provisional + Adjust** | Stock visible + precio se corrige | Lógica de ajuste |
| **Continuous (perpetual)** | Trazabilidad total | Performance con +1000 SKUs |

### Recomendación

✅ **Provisional + Adjust** — por las razones del [05](./05-estrategias-actualizacion-stock.md).

### Impacto si se cambia después

🟡 **MEDIO.** Requiere migrar la lógica de SLE provisional/finalized. Cambiar todo el modelo de auditoría. Factible pero trabajoso.

---

## Decisión 3: Tolerancia final (combinada)

### Contexto

Ya cubierto en [10 · Tolerancia de discrepancia](./10-tolerancia-discrepancia.md).

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **2% puro** | Simple | Bloquea PO pequeñas por 0,01€ |
| **2% + 5€ absoluto** | Robusto, realista | Lógica más compleja |
| **5% (estándar industria)** | Menos bloqueos | Menos estricto |

### Recomendación

✅ **2% + 5€ absoluto (lo más estricto gana)** — por las razones del [10](./10-tolerancia-discrepancia.md).

### Impacto si se cambia después

🟢 **BAJO.** Es un parámetro configurable. Cambiar el valor es trivial.

---

## Decisión 4: Over-receipt

### Contexto

Cuando llega MÁS cantidad de la pedida (ej: 1020 en vez de 1000).

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **Bloquear siempre** | Máxima seguridad | Operativo molesto |
| **Aceptar dentro de tolerancia** | Operativo | Riesgo de fraude |
| **Aceptar siempre + flag** | Flexible | Riesgo alto fraude |

### Recomendación

✅ **Aceptar dentro de tolerancia (<2%) con flag, escalar si excede.**

| Diferencia | Acción |
|------------|--------|
| <2% | Aceptar automático + flag amarillo |
| 2-10% | WARNING + aprobación nivel 2 |
| >10% | BLOQUEO + escalado a dirección |

### Impacto si se cambia después

🟢 **BAJO.** Es lógica de validación configurable.

---

## Decisión 5: Formatos de exportación prioritarios

### Contexto

Tu requisito: **varios formatos exportables**. Ya cubierto en [07 · Formatos](./07-formatos-exportacion.md).

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **PDF + XLSX + CSV** (MVP) | Cubre 95% proveedores | No EDI nativo |
| **+ XML custom** | Más interoperabilidad | Más desarrollo |
| **+ UBL / Facturae** | Estándar internacional | Mucho más desarrollo |
| **+ PEPPOL** | Compliance europeo | Coste enorme |

### Recomendación

✅ **Fase 1: PDF + XLSX + CSV + XML custom.** Cubrir el 95% de los proveedores.

Fase 2: UBL + Facturae (cuando el cliente venda a AA.PP.)

NO recomiendo PEPPOL en MVP. Coste/beneficio muy alto.

### Impacto si se cambia después

🟡 **MEDIO.** Agregar un formato nuevo es factible pero requiere:
- Plantilla del formato
- Generador
- Tests
- Documentación

---

## Decisión 6: Tipo de identificador de producto

### Contexto

Cada producto tiene un identificador único. Hay varios estándares.

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **SKU interno** | Control total | No compartible con proveedor |
| **EAN13 (código de barras europeo)** | Estándar universal | No todos los productos tienen |
| **Ambos (SKU interno + EAN13)** | Máxima flexibilidad | Lógica de matching |

### Recomendación

✅ **Ambos: SKU interno (PK) + EAN13 (opcional)**.

- SKU interno: PK en la tabla products
- EAN13: campo opcional (nullable)
- Lógica de matching:
  1. Si el proveedor manda EAN13 en su albarán, buscar por EAN13
  2. Si no, buscar por supplier_sku (código del proveedor)
  3. Si ninguno, requerir selección manual

### Impacto si se cambia después

🟡 **MEDIO.** Cambiar PK es caro, pero agregar EAN13 después es trivial.

---

## Decisión 7: Concurrencia de recepciones

### Contexto

¿Qué pasa si dos operadores (Ana y otro) reciben mercancía del mismo producto al mismo tiempo?

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **Bloqueo pesimista** (`SELECT FOR UPDATE`) | Cero race conditions | Baja concurrencia |
| **Bloqueo optimista** (versioning) | Alta concurrencia | Requiere retry logic |
| **Advisory locks** (PostgreSQL) | Flexibilidad | Complejidad |

### Recomendación

✅ **Bloqueo optimista con versioning** (campo `version` en `Stock` y `StockLot`).

```
Cada UPDATE incluye:
  - WHERE version = current_version
  - SET version = version + 1

Si retorna 0 rows → conflicto → retry o error al usuario
```

### Impacto si se cambia después

🟡 **MEDIO.** Requiere agregar campo `version` a todas las tablas. Mejor hacerlo desde el inicio.

---

## Decisión 8: Tracking de ubicaciones físicas

### Contexto

¿El sistema rastrea hasta "Pasillo 3, Estantería B" o solo "Madrid Central"?

### Opciones

| Opción | Pros | Contras |
|--------|------|---------|
| **Solo almacén** | Simple | Menos operativo |
| **Almacén + ubicación** | Picking optimizado | Más complejidad |
| **Almacén + ubicación + coordenadas** | WMS completo | Mucha complejidad |

### Recomendación

✅ **Almacén + ubicación (sin coordenadas X/Y/Z)**.

- WarehouseLocation con tipos (RECEIVING, STORAGE, PICKING, etc.)
- Stock vinculado a warehouse_id + location_id
- Sin coordenadas GPS (eso ya es WMS nivel industrial)

### Impacto si se cambia después

🟡 **MEDIO.** Agregar coordenadas después es factible pero requiere:
- Cambiar modelo de Stock
- UI de mapa del almacén
- Integración con lectores de códigos de barras

---

## 📋 Resumen de decisiones

```
┌──────────────────────────────────────────────────────────────┐
│ DECISIONES A TOMAR ANTES DE IMPLEMENTAR                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. MÉTODO DE VALORACIÓN                                     │
│    Recomendado: WAC (Moving Average)                        │
│    Impacto cambio: ALTO                                      │
│                                                              │
│ 2. ESTRATEGIA DE STOCK UPDATE                                │
│    Recomendado: Provisional + Adjust                        │
│    Impacto cambio: MEDIO                                     │
│                                                              │
│ 3. TOLERANCIA FINAL                                          │
│    Recomendado: 2% + 5€ absoluto (regla compuesta)         │
│    Impacto cambio: BAJO                                      │
│                                                              │
│ 4. OVER-RECEIPT                                             │
│    Recomendado: <2% OK + flag, 2-10% WARNING, >10% BLOQUEO│
│    Impacto cambio: BAJO                                      │
│                                                              │
│ 5. FORMATOS DE EXPORTACIÓN PRIORITARIOS                      │
│    Recomendado MVP: PDF + XLSX + CSV + XML custom          │
│    Impacto cambio: MEDIO                                     │
│                                                              │
│ 6. TIPO DE IDENTIFICADOR DE PRODUCTO                         │
│    Recomendado: SKU interno (PK) + EAN13 (opcional)        │
│    Impacto cambio: MEDIO                                     │
│                                                              │
│ 7. CONCURRENCIA DE RECEPCIONES                               │
│    Recomendado: Optimistic locking con versioning           │
│    Impacto cambio: MEDIO (si no se hace desde el inicio)    │
│                                                              │
│ 8. UBICACIONES FÍSICAS                                       │
│    Recomendado: Warehouse + Location (sin coordenadas)     │
│    Impacto cambio: MEDIO                                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🤔 Preguntas adicionales que pueden surgir

### Durante implementación

- **Multi-empresa (multi-tenant):** ¿El CRM manejará varias empresas o solo una?
- **Multi-idioma:** ¿La UI estará solo en español o también en otros?
- **Multi-moneda:** ¿Solo EUR o también otras?
- **Series de facturación:** ¿Una sola serie o múltiples (rectificativas, anticipos, etc.)?
- **Centro de costos:** ¿Cada PO/GR puede asignarse a un centro de costo o proyecto?
- **Aprobaciones paralelas:** ¿Un solo aprobador o múltiples aprobadores simultáneos?

### Después de MVP

- **Mobile app:** ¿Los operadores de almacén usan móvil o desktop?
- **Escáner de códigos:** ¿Integración con lectores de código de barras?
- **EDI integrations:** ¿Conectar directamente con sistemas de proveedores?
- **BI / Data warehouse:** ¿Necesidad de exportar datos a Power BI / Tableau / Metabase?

---

## 📋 Acción inmediata

Antes de avanzar al PRD o diseño técnico, **las 8 decisiones críticas** deben estar confirmadas por el cliente (no por mí).

Cuando me digas "implementemos esto" + las 8 decisiones confirmadas, recién ahí aplico el gate de cuestionamiento del framework para arrancar la implementación.

---

*Siguiente: [15 · Bibliografía](./15-bibliografia.md)*
