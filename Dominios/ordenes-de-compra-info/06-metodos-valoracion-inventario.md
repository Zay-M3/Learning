# 06 · Métodos de valoración de inventario

> **Cómo se calcula el precio del stock.** FIFO, LIFO, Weighted Average y Standard Cost con ejemplos numéricos.

**Creado:** Julio 2026

---

## 🎯 El problema

Cuando tenés stock de múltiples compras a distintos precios, ¿a qué precio valorás cada unidad?

```
Compra 1: 100 unidades a $10
Compra 2: 100 unidades a $12

Venta de 50 unidades → ¿qué precio uso?
¿$10 (las viejas)? ¿$12 (las nuevas)? ¿$11 (promedio)?
```

La respuesta depende del **método de valoración** que elijas. Cada uno tiene impacto fiscal y contable diferente.

---

## 📊 Los 4 métodos clásicos

### FIFO (First In, First Out)

```
Compra 1: 100 unidades a $10 (lote más viejo)
Compra 2: 100 unidades a $12
Venta: 50 unidades → salen del Lote 1
Stock restante: 50 unidades del Lote 1 ($10) + 100 del Lote 2 ($12)
Valuation rate: $11.33 (ponderado)

Uso: comida, medicamentos (compliance legal)
```

### LIFO (Last In, First Out)

```
Compra 1: 100 unidades a $10 (lote viejo)
Compra 2: 100 unidades a $12
Venta: 50 unidades → salen del Lote 2
Stock restante: 100 unidades del Lote 1 ($10) + 50 del Lote 2 ($12)
Valuation rate: $10.80 (ponderado)

⚠️ NO permitido bajo IFRS desde 2005 (pero sí bajo US GAAP)
Uso: USA, combustibles
```

### Weighted Average Cost (WAC / Moving Average)

```
Compra 1: 100 unidades a $10 → total $1000
Compra 2: 100 unidades a $12 → total $1200
Stock total: 200 unidades, valor $2200
Valuation rate: $2200 / 200 = $11.00

Recalculado en cada compra (moving) o al cierre (periodic)

Uso: el más común en ERPs modernos, distribución
```

### Standard Cost (costo estándar)

```
Definís un costo "estándar" por item ($11 estimado)
Compra real a $12 → variance = +$1 por unidad
Variance se acumula en cuenta "Purchase Price Variance"
Al final del período se ajusta contra COGS

Uso: manufactura con planificación, presupuestación
```

---

## 🎯 Recomendación para tu CRM: WAC

**Weighted Average Cost (Moving Average)** es lo que te conviene porque:

| Razón | Detalle |
|-------|---------|
| Simple | Una sola fórmula |
| Trazabilidad suficiente | Cumple PGC España |
| Maneja multi-proveedor | Natural cuando hay variantes de precio |
| Fácil de explicar | Un usuario lo entiende sin contadores |
| Sin lot tracking | No necesitás serializar cada lote |

---

## 📐 Cálculo WAC paso a paso

### Fórmula

```
WAC_nuevo = (Valor_stock_anterior + Valor_compra_actual)
           / (Cantidad_stock_anterior + Cantidad_compra_actual)
```

### Ejemplo completo

```
ESTADO INICIAL:
  Stock: 0 uds
  WAC: 0 €/u

COMPRA 1 (Ana confirma GR, 2026-07-01):
  Cantidad: 200 uds
  Precio PO: 0,14€/u
  Valor: 200 × 0,14 = 28,00€
  
  Stock: 200 uds
  Valor total: 28,00€
  WAC: 0,14€/u

COMPRA 2 (Ana confirma GR, 2026-07-18):
  Cantidad: 1000 uds
  Precio PO: 0,15€/u (provisional)
  Valor: 1000 × 0,15 = 150,00€
  
  Cálculo nuevo WAC:
    Valor total: 28,00 + 150,00 = 178,00€
    Cantidad: 200 + 1000 = 1200 uds
    WAC: 178,00 / 1200 = 0,1483€/u
  
  Stock: 1200 uds
  Valor total: 178,00€
  WAC: 0,1483€/u

AJUSTE POR INVOICE (Laura carga factura, 2026-07-19):
  Precio real factura: 0,148€/u (descuento comercial)
  Valor real: 1000 × 0,148 = 148,00€
  Ajuste: -2,00€ (de 150,00 a 148,00)
  
  Cálculo nuevo WAC:
    Valor total: 28,00 + 148,00 = 176,00€
    Cantidad: 1200 uds
    WAC: 176,00 / 1200 = 0,1467€/u
  
  Stock: 1200 uds
  Valor total: 176,00€
  WAC: 0,1467€/u

VENTA (operación normal, 2026-07-20):
  Cantidad vendida: 300 uds
  Precio venta: 0,50€/u
  WAC actual: 0,1467€/u
  COGS: 300 × 0,1467 = 44,00€
  Margen bruto: 300 × (0,50 - 0,1467) = 106,00€
  
  Stock: 900 uds
  Valor total: 900 × 0,1467 = 132,00€
  WAC: 0,1467€/u (NO cambia con ventas)
```

---

## 🧮 Implementación algorítmica

### Pseudocódigo WAC con provisional+adjust

```
function receive_stock(product_id, warehouse_id, qty, provisional_price):
    # Obtener stock actual
    current = get_stock(product_id, warehouse_id)

    # Calcular nuevo WAC (provisional)
    new_qty = current.qty + qty
    new_value = current.value + (qty * provisional_price)
    new_wac = new_value / new_qty

    # Actualizar stock
    update_stock(product_id, warehouse_id, qty=new_qty, value=new_value, wac=new_wac)

    # Crear SLE provisional
    create_sle({
        product_id: product_id,
        warehouse_id: warehouse_id,
        qty_change: qty,
        value_change: qty * provisional_price,
        provisional: true,
        source_type: 'GR',
        source_id: gr_id
    })

function invoice_adjustment(product_id, warehouse_id, gr_id, real_price):
    # Encontrar SLE provisional relacionado
    provisional_sle = find_sle(source_id=gr_id, provisional=true)
    qty = provisional_sle.qty_change
    provisional_value = provisional_sle.value_change
    real_value = qty * real_price

    delta = real_value - provisional_value  # usualmente negativo

    # Crear SLE de ajuste (sin cambio de cantidad)
    create_sle({
        product_id: product_id,
        warehouse_id: warehouse_id,
        qty_change: 0,
        value_change: delta,
        provisional: false,
        source_type: 'INVOICE_ADJUSTMENT',
        source_id: gr_id
    })

    # Marcar SLE provisional como finalized
    update_sle(provisional_sle.id, finalized=true)

    # Recalcular WAC
    current = get_stock(product_id, warehouse_id)
    new_wac = current.value / current.qty
    update_stock(product_id, warehouse_id, wac=new_wac)
```

---

## ⚠️ Casos especiales

### Stock con valor 0 (muestras gratis, regalos)

```
Si precio_factura = 0:
  - WAC no se ve afectado (delta = 0)
  - Pero requiere flag especial para auditoría
  - Cuenta contable 609 (Rappels) o 778 (ingresos extraordinarios)
```

### Devolución a proveedor

```
Si se devuelven N unidades:
  - SLE: -N uds @ WAC actual
  - Stock: Stock_actual - N
  - WAC NO cambia (operación de mismas unidades)
  
  Si el proveedor devuelve el dinero:
    - Asiento: 400 Proveedores (DEBE) / 700 Ventas (HABER) [negativo]
    - O 600 Compras (HABER) si se considera corrección
```

### Stock negativo (error de sistema)

```
Si por error stock < 0:
  - Bloquear venta
  - Forzar reconciliación (stock count físico)
  - Generar SLE de ajuste con cuenta "pérdida stock"
```

---

## 📊 Comparativa final

| Criterio | FIFO | LIFO | WAC | Standard |
|----------|------|------|-----|----------|
| Simplicidad | Media | Media | Alta | Baja |
| Trazabilidad lote | Alta | Alta | Baja | Baja |
| Realidad económica | Alta (en inflación) | Alta (deflación) | Media | Baja |
| Compliance IFRS | ✅ | ❌ | ✅ | ✅ |
| Compliance US GAAP | ✅ | ✅ | ✅ | ✅ |
| España (PGC) | ✅ | ❌ (no recomendado) | ✅ | ✅ |
| Performance con +1000 SKUs | Media | Media | Alta | Alta |
| Multi-proveedor | Media | Media | Alta | Media |

**Recomendación final: WAC (Weighted Average Cost)** para tu CRM.

---

## 📚 Referencias

- Wikipedia: [Inventory valuation](https://en.wikipedia.org/wiki/Inventory_valuation)
- Wikipedia: [Material requirements planning](https://en.wikipedia.org/wiki/Material_requirements_planning)

---

*Siguiente: [07 · Formatos de exportación](./07-formatos-exportacion.md)*
