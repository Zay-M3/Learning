---
session: Dominios
title: "Multi-proveedor con variantes de precio"
---

# 08 · Multi-proveedor con variantes de precio

> **Mismo producto, distintos proveedores, distintos precios.** Cómo se modela, cómo se elige proveedor, cómo se calcula el coste.

**Creado:** Julio 2026

---

## 🎯 El problema

En la realidad, un mismo producto **SIEMPRE** puede venir de varios proveedores a precios distintos:

```
Producto: Tornillo M8x30 galvanizado (SKU: TORN-M8-30-GAL)

Proveedor A "García":      0,15€/ud   (entrega 5 días)
Proveedor B "Sur":          0,18€/ud   (entrega 3 días, mejor calidad)
Proveedor C "Norte":        0,14€/ud   (entrega 7 días, peor calidad)
Proveedor D "Químicos":     0,155€/ud  (entrega 10 días, especial)
```

El sistema debe poder:
1. Rastrear qué precio tiene cada proveedor
2. Sugerir el mejor proveedor según contexto
3. Calcular el coste agregado del stock
4. Reportar savings si compras más a Norte

---

## 🗃️ Modelo de datos

### Tabla `Product` (maestro de productos)

```
Product:
  - id (PK)
  - sku (TORN-M8-30-GAL)
  - name (Tornillo M8x30 galvanizado)
  - description
  - category_id (FK → Category)
  - unit_of_measure (EA, KG, M, L, etc.)
  - hs_code (código arancelario, si aplica)
  - country_of_origin
  - active (bool)
  - created_at
  - updated_at
```

### Tabla `Supplier` (maestro de proveedores)

```
Supplier:
  - id (PK)
  - cif (B-87654321)         -- único
  - name (Suministros García)
  - payment_terms_days (30)
  - currency (EUR)
  - preferred_format (PDF, XLSX, Facturae, etc.)
  - email (pedidos@garcia.com)
  - phone
  - address
  - iban (ES91 2100 0418 4502 0005 1332)
  - active (bool)
  - rating (1-5 estrellas, opcional)
  - created_at
  - updated_at
```

### Tabla `SupplierProduct` (relación producto↔proveedor)

```
SupplierProduct:
  - id (PK)
  - supplier_id (FK → Supplier)
  - product_id (FK → Product)
  - supplier_sku (GARCIA-TORN-30)  -- código del proveedor
  - supplier_product_name           -- nombre del proveedor
  - last_purchase_price (0.15)
  - last_purchase_date (2026-07-15)
  - min_order_quantity (1)
  - lead_time_days (5)
  - preferred_supplier (bool)       -- para sugerencias automáticas
  - active (bool)
  - created_at
  - updated_at
```

### Tabla `Stock` (stock por producto/almacén)

```
Stock:
  - id (PK)
  - product_id (FK → Product)
  - warehouse_id (FK → Warehouse)
  - location_id (FK → WarehouseLocation, nullable)
  - quantity (1200)
  - wac_unit_cost (0.1467)         -- WAC del stock actual
  - updated_at
```

### Tabla `StockLot` (opcional, para trazabilidad por lote)

```
StockLot:
  - id (PK)
  - product_id
  - warehouse_id
  - supplier_id                    -- quién lo proveyó
  - supplier_lot_reference
  - quantity
  - unit_cost                      -- precio ORIGINAL de compra (no WAC)
  - received_date
  - expiry_date (nullable)
```

---

## 🤖 Algoritmo de selección de proveedor

### Selección manual

```
El usuario (Carlos) selecciona proveedor desde dropdown.
Simple, pero requiere conocimiento del usuario.
```

### Selección automática (sugerencia)

```
function suggest_supplier(product_id, quantity, target_warehouse_id):
    candidates = SupplierProduct
        .where(product_id, active=true)
        .order_by(score DESC)
        .limit(3)
        .get()

    for each candidate in candidates:
        score = 0

        # 1. Precio (40% peso)
        if candidate.last_purchase_price <= average_price:
            score += 40 * (1 - variance)
        else:
            score += 40 * (1 - (variance * 2))

        # 2. Lead time (30% peso)
        if candidate.lead_time_days <= target_days:
            score += 30
        else:
            score += 30 * (1 - penalty)

        # 3. Proveedor preferente (15% peso)
        if candidate.preferred_supplier:
            score += 15

        # 4. Historial de cumplimiento (15% peso)
        score += 15 * (on_time_delivery_rate)

        candidate.score = score

    return candidates  -- ordenados por score
```

### Selección por reglas (configurable)

```
Empresa puede definir reglas custom:
  - "Para > 5000 unidades, siempre usar Norte"
  - "Para entregas urgentes (< 3 días), usar Sur"
  - "Para productos certificados, usar Químicos"
  
Implementación: tabla supplier_selection_rules con priority
```

---

## 💰 Cálculo de coste multi-proveedor

### Stock agregado de un producto

```
Producto: TORN-M8-30-GAL
Origen del stock actual:

┌──────────────────────────────────────────────────────┐
│ Lote    │ Proveedor │ Cant │ Precio/u │ Valor       │
├──────────────────────────────────────────────────────┤
│ LOTE-01 │ García    │ 200  │ 0,14€    │  28,00€     │
│ LOTE-02 │ García    │ 1000 │ 0,148€   │ 148,00€     │
│ LOTE-03 │ Sur       │ 500  │ 0,15€    │  75,00€     │
│ LOTE-04 │ Norte     │ 300  │ 0,147€   │  44,10€     │
│ LOTE-05 │ García    │ 400  │ 0,148€   │  59,20€     │
├──────────────────────────────────────────────────────┤
│ TOTAL   │           │ 2400 │          │ 354,30€     │
└──────────────────────────────────────────────────────┘

WAC = 354,30 / 2400 = 0,1476€/u
```

### Reporte de savings potencial

```
┌──────────────────────────────────────────────────────────┐
│ SUGERENCIA DE OPTIMIZACIÓN                               │
├──────────────────────────────────────────────────────────┤
│ Producto: TORN-M8-30-GAL                                │
│ Proveedor actual principal: García (38% volumen)         │
│ Mejor precio histórico: Norte (0,147€/u)                │
│                                                          │
│ Si cambias 30% del volumen de García a Norte:           │
│   Actual:   30% × 2400 uds × 0,148€/u = 106,56€        │
│   Propuesto: 30% × 2400 uds × 0,147€/u = 105,84€      │
│   Ahorro mensual: 0,72€                                 │
│                                                          │
│ ⚠️ Considerar: lead time Norte = 7 días vs García = 5  │
│ ⚠️ Considerar: calidad (Norte tiene peor rating)       │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 KPIs multi-proveedor

### Por producto

| KPI | Fórmula | Ejemplo |
|-----|---------|---------|
| Proveedor principal | Top 1 por volumen | García (38%) |
| Spread de precios | (max - min) / min × 100 | (0,18 - 0,14) / 0,14 = 28,6% |
| Precio promedio | Avg de últimos N meses | 0,153€/u |
| # proveedores activos | Count distinct | 4 |

### Por proveedor

| KPI | Fórmula | Ejemplo |
|-----|---------|---------|
| Volumen comprado | Suma qty últimos N meses | 9.500 uds |
| Valor comprado | Suma importe últimos N meses | 1.425€ |
| Ticket medio | Valor / # POs | 178€ |
| On-time delivery rate | # entregas OK / # entregas total | 92% |
| Quality rate | # sin defectos / # total recibidas | 96% |
| Lead time medio | Avg días desde PO hasta GR | 5,2 días |

---

## 🧪 Casos edge

### Cambio de proveedor preferente

```
Escenario: García sube precio a 0,17€/u
Recomendación: Norte ahora es mejor precio

Implementación:
  1. Sistema detecta cambio de spread
  2. Alerta a Carlos: "García subió +13%. Norte ahora es mejor opción"
  3. Carlos puede:
     a. Cambiar preferred_supplier a Norte
     b. Mantener García si tiene otras razones (lead time, calidad)
     c. Negociar con García
```

### Proveedor discontinuado

```
Escenario: Norte deja de vender TORN-M8-30-GAL

Implementación:
  1. Carlos marca SupplierProduct.active = false para Norte
  2. Stock actual de Norte sigue siendo válido
  3. Futuras POs no sugieren a Norte para ese producto
  4. Histórico preservado para auditoría
```

### Proveedor nuevo

```
Escenario: Agregar "Distribuciones Este" como proveedor nuevo

Implementación:
  1. Crear Supplier con CIF único
  2. Crear SupplierProduct vinculando a productos existentes
  3. last_purchase_price = null (aún sin compras)
  4. preferred_supplier = false (no es preferente hasta tener histórico)
  5. Sistema empieza a trackear desde la primera PO
```

---

## 📐 Implementación algorítmica del WAC multi-proveedor

```
function calculate_wac_multi_supplier(product_id, warehouse_id):
    lots = StockLot.where(product_id, warehouse_id, quantity > 0)

    total_qty = sum(lot.quantity for lot in lots)
    total_value = sum(lot.quantity * lot.unit_cost for lot in lots)

    if total_qty == 0:
        return (0, 0)  # sin stock

    wac = total_value / total_qty
    return (wac, total_value)

# Cuando llega nueva compra:
function add_new_lot(product_id, warehouse_id, supplier_id, qty, price):
    new_lot = StockLot(
        product_id=product_id,
        warehouse_id=warehouse_id,
        supplier_id=supplier_id,
        quantity=qty,
        unit_cost=price,
        received_date=now()
    )
    new_lot.save()

    # Recalcular WAC
    (wac, value) = calculate_wac_multi_supplier(product_id, warehouse_id)
    update_stock(product_id, warehouse_id, wac=wac, value=value)
```

---

## 📚 Referencias

- Wikipedia: [Vendor-managed inventory](https://en.wikipedia.org/wiki/Vendor-managed_inventory) (modelo alternativo)
- Wikipedia: [Inventory valuation](https://en.wikipedia.org/wiki/Inventory_valuation)

---

*Siguiente: [09 · Multi-almacén](./09-multi-almacen.md)*
