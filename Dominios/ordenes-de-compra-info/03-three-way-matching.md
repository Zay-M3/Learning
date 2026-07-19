# 03 · Three-Way Matching (3WM)

> **El control antifraude clásico del P2P.** Por qué existe, cómo funciona, cómo lo implementan SAP/Odoo/ERPNext.

**Creado:** Julio 2026

---

## 🎯 ¿Qué es Three-Way Matching?

Es el proceso de **comparar 3 documentos** antes de autorizar un pago al proveedor:

```
┌─────────────────────┐
│ Purchase Order (PO) │  →  Pediste 100 unidades a $10 c/u = $1000
└─────────────────────┘
            ↓ coincide con ↓
┌─────────────────────┐
│ Goods Receipt (GR)  │  →  Recibiste 100 unidades a $10 c/u = $1000
└─────────────────────┘
            ↓ coincide con ↓
┌─────────────────────┐
│ Invoice del proveedor │ →  Te cobraron 100 unidades a $10 c/u = $1000
└─────────────────────┘
            ↓
   ✅ Pago autorizado

Si algo NO coincide (cantidad, precio, item):
   ❌ Discrepancia → bloquea el pago hasta resolver
```

---

## 📊 Las 4 variantes (de menos a más estricto)

| Variante | Documentos | Cuándo se usa | Riesgo que cubre |
|----------|------------|---------------|------------------|
| **1-Way** | Solo Invoice | Trivial, no recomendado | Ninguno |
| **2-Way** | PO + Invoice | Compras chicas, baja variabilidad | Cantidades fantasma |
| **3-Way** | PO + GR + Invoice | **Estándar de la industria** | Fraude, sobrestock |
| **4-Way** | + Quality Inspection | Manufactura, pharma, alimentos | Calidad defectuosa |

---

## 🏗️ Cómo lo implementa cada ERP

### Odoo 17

> *Nota: las URLs oficiales de Odoo 17 (odoo.com/documentation/17.0) devolvieron 403 durante la investigación desde este entorno. Esta sección está basada en documentación pública y experiencia de implementación.*

El flujo en Odoo:
1. PO crea `expected_qty` por línea
2. GR (llamado "Receipt" en Odoo) crea `received_qty`
3. Vendor Bill (invoice) crea `billed_qty`
4. Sistema compara las 3 cantidades y flag discrepancies:
   - `received_qty > ordered_qty` → over-receipt (alerta)
   - `billed_qty > received_qty` → posible fraude (bloquea pago)
   - `received_qty ≠ billed_qty` → discrepancy (requiere aprobación)
5. Tolerancia configurable por item (ej: ±2%)

### SAP Business One / S/4HANA

SAP usa el concepto **"Logistics Invoice Verification" (LIV)**:

- PO = `purchase order` con `gr_quantity`
- GR = `goods receipt` con `gr_value`
- Invoice = `vendor invoice` con `invoice_value`
- Sistema hace 3 checks automáticos:
  - **Quantities match:** GR qty = Invoice qty
  - **Prices match:** PO price = Invoice price (con tolerance)
  - **Calculations match:** Total = sum(price × qty)

Si todo coincide → bloquea para pago. Si no → bloquea para **resolución manual** por un usuario autorizado.

### ERPNext

Estados de la PO reflejan el 3-way matching:

```
DRAFT → ON_HOLD → TO_RECEIVE_AND_BILL → TO_RECEIVE → TO_BILL → COMPLETED
```

### NetSuite

| Estado PO | Significado |
|-----------|-------------|
| Pending Approval | Esperando aprobador |
| Pending Receipt | PO aprobada, sin GR |
| Partially Received | GR parcial |
| Fully Received | GR completa, falta billing |
| Pending Billing | GR completa, falta invoice |
| Billed | 3WM completo |
| Closed | Cerrada |

---

## 📐 Implementación algorítmica

### Pseudocódigo del matching engine

```
function three_way_match(po, gr, invoice):
    discrepancies = []

    # CHECK 1: Cantidades por línea
    for each po_line in po.lines:
        gr_line = find gr.line matching po_line.product
        inv_line = find invoice.line matching po_line.product

        if gr_line is null:
            discrepancies.append(MISSING_GR)
            continue

        if inv_line is null:
            discrepancies.append(MISSING_INVOICE_LINE)
            continue

        if gr_line.quantity != inv_line.quantity:
            discrepancies.append(QTY_MISMATCH)

    # CHECK 2: Precios por unidad
    for each po_line in po.lines:
        inv_line = find invoice.line matching po_line.product
        if inv_line is null: continue

        price_variance_pct = abs(po_line.unit_price - inv_line.unit_price)
                            / po_line.unit_price * 100
        if price_variance_pct > TOLERANCE_PRICE_PCT:
            discrepancies.append(PRICE_VARIANCE)

    # CHECK 3: Totales
    po_total = po.total_with_tax
    inv_total = invoice.total_with_tax
    total_variance_pct = abs(po_total - inv_total) / po_total * 100

    if total_variance_pct > TOLERANCE_TOTAL_PCT:
        discrepancies.append(TOTAL_VARIANCE)

    # CHECK 4: Proveedor
    if po.supplier.cif != invoice.supplier.cif:
        discrepancies.append(SUPPLIER_MISMATCH)

    return MatchResult(
        matched = (count of blocking discrepancies == 0),
        discrepancies = discrepancies,
        blocking = (count of blocking discrepancies > 0),
        warnings = [non-blocking discrepancies]
    )
```

---

## 🎚️ Configuración de tolerancia (3 niveles)

### Nivel 1: Por línea (price variance por unidad)

```
variacion = |precio_factura - precio_PO| / precio_PO × 100
Si variacion >= 2% → WARNING
Si variacion < 2% → OK automático
```

### Nivel 2: Por línea con descuentos aplicados

```
variacion = |total_linea_factura - total_linea_PO| / total_linea_PO × 100
Si variacion >= 2% → WARNING
```

### Nivel 3: Por total de factura

```
variacion = |total_factura - total_PO| / total_PO × 100
Si variacion >= 2% → WARNING
```

### ⚠️ Recomendación para tu CRM

```
Regla primaria: variacion < 2%
Regla secundaria: variacion_absoluta < 5€
(lo que sea más estricto gana)

Justificación:
  - 2% es estricto vs industria (típico 5%)
  - 5€ absoluto cubre el caso de PO pequeñas
  - Evita que PO de 1€ se bloquee por 0,02€ de diferencia

Override:
  - Aprobador nivel 2 puede aceptar con motivo obligatorio
  - Toda override queda en audit log con hash inmutable
```

---

## 🚨 Edge cases a decidir

| Edge case | Recomendación |
|-----------|---------------|
| Diferencia EXACTA de 1.99% | Aceptar (es <2%) |
| Diferencia 2.01% | WARNING manual |
| Diferencia 50% justificada (descuento pactado en contrato) | Override con motivo |
| Diferencia 200% (10× precio) | Escalar a dirección |
| Línea con 100% descuento (muestra gratis) | NO bloquear, requiere aprobación |
| Línea con precio 0 (regalo) | NO bloquear, requiere aprobación |
| Diferencia <2% pero 0,50€ absoluto en PO de 1€ | SÍ bloquear (combinar % + mínimo) |

---

## 📚 Referencias

- Wikipedia: [Purchase-to-pay](https://en.wikipedia.org/wiki/Purchase-to-pay)
- Wikipedia: [Electronic data interchange](https://en.wikipedia.org/wiki/Electronic_data_interchange)
- Wikipedia: [Universal Business Language](https://en.wikipedia.org/wiki/Universal_Business_Language)
- Wikipedia: [PEPPOL](https://en.wikipedia.org/wiki/PEPPOL)

---

*Siguiente: [04 · Estados de la PO](./04-estados-po.md)*
