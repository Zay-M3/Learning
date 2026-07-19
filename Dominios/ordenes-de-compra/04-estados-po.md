---
session: ordenes-de-compra
title: "Estados de la Purchase Order"
---

# 04 · Estados de la Purchase Order

> **Lifecycle completo de la PO** desde borrador hasta cierre, con comparación entre SAP / Odoo / ERPNext / NetSuite.

**Creado:** Julio 2026

---

## 🎯 ¿Por qué importa el lifecycle?

Una PO no es un documento estático. Pasa por **múltiples estados** durante su vida:

```
┌─────────┐   ┌──────────┐   ┌──────────┐   ┌────────────┐   ┌─────────────┐
│  DRAFT  │ → │ APPROVED │ → │   SENT   │ → │ PARTIALLY  │ → │   CLOSED    │
└─────────┘   └──────────┘   └──────────┘   │  RECEIVED  │   └─────────────┘
     │             │              │         └────────────┘
     │             │              │              │
     │             │              │              ↓
     │             │              │         ┌─────────────┐
     │             │              │         │  COMPLETED  │
     │             │              │         └─────────────┘
     │             │              ↓
     │             │         ┌──────────┐
     │             │         │ RECEIVED │
     │             │         └──────────┘
     ↓ (cualquier estado)
┌──────────┐
│CANCELLED │
└──────────┘
```

> **Tu intuición "borrador → aprobado" encaja con el estándar universal.**

---

## 📊 Comparativa de estados por sistema

### SAP S/4HANA

```
- Open
- In Approval
- Approved
- Sent
- Partially Delivered
- Delivered
- Closed
- Cancelled
```

### Odoo 17

```
- Draft (borrador)
- RFQ (Request for Quotation)
- Sent (enviado al proveedor)
- Confirmed (confirmado, equivale a "Approved")
- Locked (bloqueado para edición)
- Purchase Order (estado terminal operativo)
- Cancelled
```

### ERPNext

```
- Draft
- On Hold
- To Receive and Bill
- To Receive
- To Bill
- Completed
- Cancelled
- Closed
```

### NetSuite

```
- Pending Approval
- Pending Receipt
- Partially Received
- Fully Received
- Pending Billing
- Billed
- Closed
```

---

## 🧩 Máquina de estados recomendada para tu CRM

### Estados principales

| Estado | Significado | Acciones permitidas | Transiciones posibles |
|--------|-------------|---------------------|------------------------|
| **DRAFT** | Borrador, editable | Editar líneas, cambiar proveedor, eliminar | → APPROVED, → CANCELLED |
| **APPROVED** | Aprobada internamente, no enviada aún | Generar PDF/XLSX/CSV | → SENT, → DRAFT (reversión), → CANCELLED |
| **SENT** | Enviada al proveedor | Marcar como acknowledged | → ACKNOWLEDGED, → PARTIALLY_RECEIVED, → RECEIVED, → CANCELLED |
| **ACKNOWLEDGED** | Proveedor confirmó recepción y aceptación | Editar cantidades si hay acuerdo | → SENT (si proveedor objeta), → PARTIALLY_RECEIVED |
| **PARTIALLY_RECEIVED** | Recepción parcial (no todas las líneas / cantidades) | Crear GRs adicionales | → RECEIVED |
| **RECEIVED** | Toda la mercancía recibida físicamente | Crear factura, validar | → INVOICED |
| **INVOICED** | Factura validada, 3WM completo | Programar pago | → PAID, → CLOSED |
| **PAID** | Pago realizado al proveedor | Cerrar PO | → CLOSED |
| **CLOSED** | PO cerrada (toda la mercancía + factura + pago OK) | Solo lectura | (estado terminal) |
| **CANCELLED** | PO cancelada en cualquier momento | Solo lectura | (estado terminal) |
| **ON_HOLD** | PO pausada por disputa o problema | Reabrir | → DRAFT, → CANCELLED |

### Transiciones explícitas

```
DRAFT ────approve───► APPROVED
DRAFT ────cancel────► CANCELLED
APPROVED ─send───► SENT
APPROVED ──revert─► DRAFT
APPROVED ─cancel─► CANCELLED
SENT ───ack────► ACKNOWLEDGED
SENT ───cancel─► CANCELLED
SENT ───partial─► PARTIALLY_RECEIVED
SENT ───full────► RECEIVED
ACKNOWLEDGED ──partial─► PARTIALLY_RECEIVED
ACKNOWLEDGED ──full───► RECEIVED
PARTIALLY_RECEIVED ──more─► PARTIALLY_RECEIVED
PARTIALLY_RECEIVED ──done► RECEIVED
RECEIVED ──invoice─► INVOICED
INVOICED ──payment─► PAID
PAID ──close────► CLOSED
ANY ──hold─────► ON_HOLD
ON_HOLD ──resume──► (vuelve al estado anterior)
```

---

## 🔐 Permisos por estado

| Estado | Carlos (Comprador) | Ana (Almacén) | Laura (Contable) |
|--------|---------------------|---------------|------------------|
| DRAFT | ✅ Editar, ✅ Eliminar | ❌ No ve | ❌ No ve |
| APPROVED | ✅ Editar campos no críticos | ❌ No ve | ❌ No ve |
| SENT | ✅ Marcar ack, ❌ Editar | ❌ No ve | ❌ No ve |
| PARTIALLY_RECEIVED | ✅ Ver, ✅ Close line | ✅ Crear GR | ❌ No ve |
| RECEIVED | ✅ Ver | ✅ Ver | ✅ Crear factura |
| INVOICED | ✅ Ver | ✅ Ver | ✅ Validar, ✅ Pagar |
| PAID | ✅ Ver | ✅ Ver | ✅ Ver |
| CLOSED | ✅ Ver (solo lectura) | ✅ Ver | ✅ Ver (solo lectura) |
| CANCELLED | ✅ Ver (solo lectura) | ✅ Ver | ✅ Ver |
| ON_HOLD | ✅ Reabrir | ❌ No ve | ❌ No ve |

---

## 🎯 Reglas de aprobación según monto

| Monto PO (sin IVA) | Aprobador requerido | Escapado a |
|--------------------|----------------------|-----------|
| < 1.000€ | Nivel 1 (Comprador mismo) | — |
| 1.000€ - 10.000€ | Nivel 2 (Manager) | Manager del comprador |
| 10.000€ - 50.000€ | Nivel 3 (Director) | Director de operaciones |
| > 50.000€ | Nivel 4 (Consejo/DG) | Comité de compras |

**Nota:** estos umbrales son configurables por empresa. Lo crítico es que existan.

---

## 🔄 Short-Close (cierre parcial)

Escenario común: pediste 100 unidades, el proveedor te avisa que solo puede enviar 80.

```
Opciones del sistema:
1. Modificar PO a 80 unidades → estado CLOSED
2. Crear PO complementaria para las 20 restantes
3. Marcar la línea como short-closed (solo cierra esa línea)
```

**Implementación típica:** modificar `quantity_ordered` al valor real recibido. Mantiene la trazabilidad de que originalmente se pidieron 100.

---

## 🚫 Cancelación en distintos estados

| Estado al cancelar | Efecto en stock | Efecto contable |
|--------------------|-----------------|-----------------|
| DRAFT | Ninguno | Ninguno |
| APPROVED | Ninguno | Ninguno |
| SENT | Ninguno | Ninguno |
| PARTIALLY_RECEIVED | Revierte SLE parcial | Asiento de reversión |
| RECEIVED | Revierte SLE completo | Asiento de reversión |
| INVOICED | Revierte SLE + asiento factura | Asiento de reversión total |
| PAID | Requiere proceso manual con proveedor | Nota de crédito + devolución |

---

## 📚 Referencias

- Wikipedia: [Purchase order](https://en.wikipedia.org/wiki/Purchase_order)
- Wikipedia: [Purchase-to-pay](https://en.wikipedia.org/wiki/Purchase-to-pay)

---

*Siguiente: [05 · Estrategias de actualización de stock](./05-estrategias-actualizacion-stock.md)*
