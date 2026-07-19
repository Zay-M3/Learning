# 05 · Estrategias de actualización de stock

> **Cuándo se actualiza el stock en el sistema.** Las 4 estrategias que usa la industria, con pros/cons y ejemplos por sector.

**Creado:** Julio 2026

---

## 🎯 La pregunta clave

**¿En qué momento exacto se actualiza el stock del sistema cuando llega mercancía?**

Parece trivial, pero la respuesta cambia el comportamiento completo del ERP. La industria ha desarrollado 4 estrategias diferentes.

---

## 📊 Las 4 estrategias

### A) Update on Receipt (al recibir)

```
GR llega → actualizar stock inmediatamente
Invoice llega después → SOLO comparar precios (sin tocar stock)

+ Pros:
  - Stock siempre refleja realidad física
  - Más simple de implementar
- Cons:
  - Precio puede no ser exacto hasta factura
  - Si invoice no llega, hay items sin precio
```

### B) Update on Invoice (estricto)

```
GR llega → marcar como "received but not valued"
Invoice llega → comparar GR vs Invoice → si OK, actualizar stock + precio

+ Pros:
  - Stock SIEMPRE tiene precio real (cero discrepancia)
  - Cumple GAAP/IFRS estrictamente
- Cons:
  - Stock "invisible" hasta que llegue invoice
  - Si proveedor tarda en facturar, stock no aparece
```

### C) Update Provisional + Adjust on Invoice (la más común)

```
GR llega → actualizar stock con precio PROVISIONAL (del PO)
         → marcar "provisional valuation"
Invoice llega → comparar vs provisional
             → si difiere: ajustar con "Invoice Adjustment"
             → recalcular valuation rate

+ Pros:
  - Stock disponible inmediatamente
  - Precio se corrige cuando llega factura
  - Equilibrio entre velocidad y precisión
- Cons:
  - Requiere lógica de ajuste posterior
  - Pequeñas discrepancias contables temporales
```

### D) Continuous Update (perpetual)

```
Cada movimiento (GR, Return, Transfer) → SLE inmediato
Sistema calcula cost layer usando método configurado
FIFO/LIFO/Weighted Average recalculan automáticamente

+ Pros:
  - Trazabilidad total, ideal para manufactura
  - Costo siempre actualizado
- Cons:
  - Requiere Stock Ledger complejo
  - Performance degrada con millones de SKUs
```

---

## 🏭 Qué estrategia usa cada industria

| Industria | Estrategia típica | Razón |
|-----------|-------------------|-------|
| **Retail** (Walmart, Zara) | **Update on Receipt** | Velocidad > exactitud, millones de items/día |
| **Manufactura** (Boeing, Toyota) | **Continuous (perpetual)** | Trazabilidad por serial/lote obligatoria |
| **Distribución** (Coca-Cola) | **Provisional + Adjust** | Mix de velocidad + accuracy |
| **Pharma/Medical** | **Update on Invoice + 4-Way** | Compliance regulatorio (FDA, EMA) |
| **Construcción** | **2-Way (PO + Invoice)** | Items únicos, no necesitan stock perpetuo |
| **Alimentos** | **Provisional + Adjust** con lotes | Trazabilidad + velocidad |

---

## 🎯 Tu caso: recomendación

**Estrategia C: Provisional + Adjust**

Razones:
1. Tu CRM maneja stock físico real → necesitas que esté visible
2. Proveedores pueden tardar en facturar → no podés esperar
3. Es lo que hacen SAP, Odoo, ERPNext por defecto
4. Encaja con tu tolerancia <2%

---

## 📐 Implementación: Provisional + Adjust

### Paso 1: Recepción provisional

```
Cuando Ana confirma la GR:
  - SLE: +1000 unidades @ 0,15€/u = +150,00€ (precio del PO)
  - Stock value: 1200 uds @ 0,1483€/u = 178,00€
  - SLE.provisional = true
  - SLE.source_po = PO_2026_0042
```

### Paso 2: Llegada de factura con precio distinto

```
Cuando Laura carga la factura GARCIA-FAC-2026-1523:
  - Precio real: 0,148€/u (no 0,15€/u)
  - Variance: -0,002€/u × 1000 uds = -2,00€ (favorable)

El sistema:
  1. Encuentra SLEs provisionales relacionados con esta factura
  2. Calcula el delta
  3. Genera SLE de ajuste:
     SLE_2026_7891_adjustment: -2,00€
  4. Recalcula WAC del producto:
     Stock value: 1200 uds @ 0,1467€/u = 176,00€
  5. Marca SLE original como finalized
```

### Paso 3: Trazabilidad

```
Cada SLE mantiene:
  - id_sle
  - product_id
  - warehouse_id
  - qty_change
  - valuation_change
  - provisional: bool
  - source_type: 'GR' | 'INVOICE_ADJUSTMENT' | 'TRANSFER' | 'RETURN' | 'ADJUSTMENT'
  - source_id: <id del documento>
  - created_at
  - finalized_at (cuando deja de ser provisional)
  - created_by
```

---

## 🧮 Ejemplo completo

```
ESCENARIO:
  Producto: TORN-M8-30-GAL
  Stock previo Madrid: 200 uds @ 0,14€/u = 28,00€
  
  PO #PO_2026_0042: 1000 uds @ 0,15€/u
  
GR CONFIRMADA (Ana, 2026-07-18):
  SLE_1: +1000 uds @ 0,15€/u = +150,00€ (provisional)
  Stock: 1200 uds @ 178,00€ → WAC = 0,1483€/u
  
INVOICE RECIBIDA (Laura, 2026-07-19):
  Precio real: 0,148€/u (descuento comercial)
  Total: 148,00€ + 30,46€ IVA = 178,46€ (con dto 2,96€)
  
AJUSTE AUTOMÁTICO (sistema):
  SLE_2: 0 uds @ 0,002€/u = -2,00€ (adjustment)
  Stock: 1200 uds @ 176,00€ → WAC = 0,1467€/u
  
ASIENTO CONTABLE:
  600 Compras       148,00€ (DEBE)
  472 IVA soportado  30,46€ (DEBE)
  400 Proveedores   178,46€ (HABER)
  
  300 Mercaderías    +2,00€ (DEBE)  -- ajuste
  798 Var. precio     2,00€ (HABER)
```

---

## ⚠️ Anti-patrones

### ❌ Anti-patrón 1: Stock solo cuando llega invoice

```
"Ana recibe la mercancía pero no la vemos en el sistema hasta que llegue la factura"
- Stock "fantasma" durante días/semanas
- Imposible planificar ventas
- Genera trabajo manual de "lo que sé que llegó pero el sistema no registra"
```

### ❌ Anti-patrón 2: Precio hardcoded del PO sin ajuste

```
"El stock se queda con el precio del PO para siempre"
- Enmascara la realidad contable
- Dificulta auditoría
- PPV (Purchase Price Variance) se acumula sin control
```

### ❌ Anti-patrón 3: SLE sin trazabilidad

```
"Solo guardo el stock total, no los movimientos individuales"
- Imposible auditar
- Imposible revertir operaciones
- debugging imposible
```

---

## 📚 Referencias

- Wikipedia: [Inventory valuation](https://en.wikipedia.org/wiki/Inventory_valuation)
- Wikipedia: [Warehouse management system](https://en.wikipedia.org/wiki/Warehouse_management_system)
- Wikipedia: [Material requirements planning](https://en.wikipedia.org/wiki/Material_requirements_planning)

---

*Siguiente: [06 · Métodos de valoración de inventario](./06-metodos-valoracion-inventario.md)*
