---
session: Dominios
title: "Reportes operativos (KPIs y dashboards)"
---

# 12 · Reportes operativos (KPIs y dashboards)

> **Lo que necesita Carlos (Compras) y Ana (Almacén)** para operar el día a día. Dashboards, alertas, KPIs.

**Creado:** Julio 2026

---

## 🎯 Diferencia con reportes contables

```
Reportes CONTABLES (Laura) → Cumplimiento legal, fiscal, auditoría
Reportes OPERATIVOS (Carlos, Ana) → Decisiones del día a día, performance
```

Los reportes operativos son para **actuar**, los contables son para **declarar**.

---

## 📊 Dashboard principal de Compras (Carlos)

### Vista "Mi día a día"

```
┌──────────────────────────────────────────────────────────────┐
│ DASHBOARD COMPRAS — Carlos Martín — 2026-07-19              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ACCIONES PENDIENTES:                                         │
│   📋 POs por aprobar:           3   (urgente: 1)             │
│   💰 POs por enviar:            5                            │
│   ⚠️  Discrepancias abiertas:   2   (1 bloqueante)          │
│   📞 Proveedores contactados:   0                            │
│                                                              │
│ KPIs DEL MES:                                                │
│   POs creadas:                  47                            │
│   Valor total comprado:         24.580€                      │
│   Ticket medio:                 523€                         │
│   On-time delivery rate:        92%                          │
│                                                              │
│ TOP PROVEEDORES (por valor):                                 │
│   1. García          9.260€ (38%)                            │
│   2. Sur Metalúrgica 5.880€ (24%)                           │
│   3. Distribución N. 4.450€ (18%)                           │
│   4. Químicos Sur    2.940€ (12%)                           │
│   5. Otros           2.050€ (8%)                            │
│                                                              │
│ ALERTAS:                                                     │
│   🔴 Norte subió precio 8% esta semana                       │
│   🟡 Sur tiene lead time degradado (3→5 días)               │
│   🟢 García cumple SLA consistentemente                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Dashboard de Almacén (Ana)

### Vista "Recepciones del día"

```
┌──────────────────────────────────────────────────────────────┐
│ DASHBOARD ALMACÉN MADRID — Ana López — 2026-07-19           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ HOY:                                                        │
│   Recepciones esperadas:     4                                │
│   Recepciones completadas:   2                                │
│   Pendientes de validar:     2                                │
│                                                              │
│ RECEPCIONES PENDIENTES:                                      │
│ ┌────────────────────────────────────────────────────┐      │
│ │ Hora │ Proveedor    │ PO         │ Estado          │      │
│ ├────────────────────────────────────────────────────┤      │
│ │ 14:00│ García       │ PO_0042    │ 🟡 Validando   │      │
│ │ 16:30│ Sur          │ PO_0051    │ ⚪ Esperando   │      │
│ └────────────────────────────────────────────────────┘      │
│                                                              │
│ STOCK BAJO MÍNIMO (alertas):                                 │
│   🔴 TORN-M8-30-GAL:     120 uds (mín: 500)               │
│   🔴 TUE-10-AZUL:        45 uds (mín: 200)                │
│   🟡 ARAN-M8-30-GAL:    180 uds (mín: 200)                │
│                                                              │
│ INCIDENCIAS ABIERTAS:                                        │
│   ⚠️ 1 producto dañado en Q-1 (pendiente RMA)              │
│   ⚠️ 1 transferencia en tránsito desde Barcelona           │
│                                                              │
│ KPIs DEL MES:                                                │
│   Recepciones totales:        87                             │
│   On-time validation:         96%                            │
│   Exactitud inventario:       99,2%                          │
│   Recepciones con discrepancia: 3 (3,4%)                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Dashboard Ejecutivo (Dirección)

### Vista "Performance global"

```
┌──────────────────────────────────────────────────────────────┐
│ DASHBOARD EJECUTIVO — Julio 2026                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ COMPRAS:                                                     │
│   Volumen total:          24.580€  (↑ 12% vs mes anterior) │
│   # POs:                  47        (↑ 8% vs mes anterior)  │
│   Ticket medio:           523€      (↑ 4% vs mes anterior)  │
│   Proveedores activos:    12        (sin cambios)            │
│                                                              │
│ INVENTARIO:                                                  │
│   Valor stock:            45.678€   (↑ 5% vs mes anterior) │
│   Items en stock:         1.234                                │
│   Rotación (DSI):         18 días    (objetivo: 15 días)   │
│   Stock obsoleto:         2,3%       (objetivo: <5%) ✅     │
│                                                              │
│ OPERACIONES:                                                 │
│   On-time delivery (recepción):    92% (objetivo: >90%) ✅ │
│   On-time invoicing (pago):        96% (objetivo: >95%) ✅ │
│   Discrepancias no resueltas:      2                         │
│   Errores de inventario:           0                         │
│                                                              │
│ FINANZAS:                                                    │
│   PPV (Purchase Price Variance):  +127€  (desfavorable)     │
│   PPV vs presupuesto:            -0,3% (dentro de meta) ✅ │
│   Plazo medio de pago:            28 días                   │
│   Plazo medio de cobro (clientes): 45 días                  │
│   Working capital:                15.000€                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📈 KPIs principales por categoría

### Compras

| KPI | Fórmula | Objetivo típico |
|-----|---------|-----------------|
| **Volumen comprado** | Suma importe POs del período | — |
| **# POs creadas** | Count POs del período | — |
| **Ticket medio** | Volumen / # POs | Depende de industria |
| **% POs urgentes** | POs urgentes / total POs | <10% |
| **On-time approval** | POs aprobadas en SLA / total | >95% |
| **On-time delivery** | GRs en fecha esperada / total | >90% |
| **On-time invoicing** | Invoices recibidas en plazo / total | >95% |
| **% POs con discrepancia** | POs con discrepancies / total | <5% |
| **% POs canceladas** | POs canceladas / total | <2% |

### Proveedores

| KPI | Fórmula | Objetivo típico |
|-----|---------|-----------------|
| **On-time delivery rate** | Entregas OK / total entregas | >90% |
| **Quality rate** | Items sin defectos / total recibidos | >95% |
| **Lead time medio** | Avg días PO → GR | Depende del proveedor |
| **Variabilidad lead time** | StdDev lead time | Lo menor posible |
| **Fill rate** | Items completos vs pedidos | >98% |
| **PPV promedio** | Avg(Precio Factura - Precio PO) por item | ~0% |
| **Concentration risk** | % compras al top 3 proveedores | <60% |

### Inventario

| KPI | Fórmula | Objetivo típico |
|-----|---------|-----------------|
| **DSI (Days Sales of Inventory)** | (Stock medio / Coste ventas) × 365 | 15-30 días |
| **Stock turnover** | Coste ventas / Stock medio | 8-20× año |
| **% Stock obsoleto** | Stock sin movimiento >180 días / total | <5% |
| **% Stock bajo mínimo** | Items bajo stock mínimo / total | <3% |
| **Exactitud inventario** | Items con count correcto / total items | >98% |
| **% Out-of-stock** | Días sin stock / total días | <1% |

### Financieros

| KPI | Fórmula | Objetivo típico |
|-----|---------|-----------------|
| **PPV total** | Suma variance PO vs Invoice | ~0 |
| **% PPV vs presupuesto** | PPV / presupuesto | <2% |
| **DPO (Days Payable Outstanding)** | (Proveedores / Compras) × 365 | 30-60 días |
| **Cash conversion cycle** | DSO + DSI - DPO | Lo menor posible |
| **Working capital** | Stock + Clientes - Proveedores | Depende del sector |

---

## 🚨 Sistema de alertas

### Configuración de umbrales

```yaml
alerts:
  stock_bajo_minimo:
    threshold: stock < min_stock
    severity: high
    notify: ["compras", "almacen_responsable"]
    
  sobreprecio_proveedor:
    threshold: variacion_pct > 5%
    severity: medium
    notify: ["compras"]
    
  factura_pendiente_validar:
    threshold: dias > 5
    severity: medium
    notify: ["contabilidad"]
    
  recepcion_pendiente_validar:
    threshold: horas > 24
    severity: medium
    notify: ["almacen_responsable"]
    
  transferencia_en_transito:
    threshold: dias > 3
    severity: medium
    notify: ["almacen_origen", "almacen_destino"]
    
  po_vencida:
    threshold: dias > 30 sin recibir
    severity: high
    notify: ["compras", "direccion"]
```

### Canales de notificación

```
- Email (siempre)
- SMS (solo críticos)
- Push notification (si mobile app)
- Webhook a Slack/Teams
- Dashboard badge
```

---

## 📊 Reportes pre-calculados

### Reporte diario (automatizado)

```
Reporte: "Estado diario de compras"
Frecuencia: 8:00 AM cada día
Destinatarios: Carlos (Compras), Ana (Almacén)
Contenido:
  - POs creadas ayer
  - GRs confirmadas ayer
  - Invoices recibidas ayer
  - POs pendientes por estado
  - Top 3 alertas activas
```

### Reporte semanal

```
Reporte: "Performance semanal"
Frecuencia: lunes 9:00 AM
Destinatarios: Carlos, Ana, Laura
Contenido:
  - KPIs de la semana vs objetivo
  - Top proveedores
  - Discrepancias abiertas
  - Stock bajo mínimo
```

### Reporte mensual

```
Reporte: "Cierre mensual operativo"
Frecuencia: primer día del mes siguiente
Destinatarios: Carlos, Ana, Laura, Dirección
Contenido:
  - KPIs del mes
  - Variaciones vs presupuesto
  - Top performers / underperformers
  - Recomendaciones automáticas
```

---

## 📊 Vistas SQL pre-calculadas (ejemplos)

### Vista: Stock actual por producto/almacén

```sql
CREATE VIEW v_stock_current AS
SELECT
    p.id AS product_id,
    p.sku,
    p.name AS product_name,
    w.id AS warehouse_id,
    w.code AS warehouse_code,
    w.name AS warehouse_name,
    s.quantity,
    s.reserved_quantity,
    s.available_quantity,
    s.wac_unit_cost,
    s.quantity * s.wac_unit_cost AS total_value,
    s.updated_at
FROM products p
JOIN stock s ON s.product_id = p.id
JOIN warehouses w ON w.id = s.warehouse_id
WHERE s.quantity > 0;
```

### Vista: POs pendientes

```sql
CREATE VIEW v_pending_pos AS
SELECT
    po.id AS po_id,
    po.number,
    po.status,
    s.cif AS supplier_cif,
    s.name AS supplier_name,
    po.created_at,
    po.expected_delivery_date,
    po.total_with_tax,
    DATEDIFF(day, po.expected_delivery_date, GETDATE()) AS days_overdue
FROM purchase_orders po
JOIN suppliers s ON s.id = po.supplier_id
WHERE po.status IN ('SENT', 'ACKNOWLEDGED', 'PARTIALLY_RECEIVED')
    AND po.status != 'CLOSED';
```

### Vista: Top proveedores por valor

```sql
CREATE VIEW v_top_suppliers AS
SELECT
    s.id AS supplier_id,
    s.cif,
    s.name AS supplier_name,
    COUNT(DISTINCT po.id) AS po_count,
    SUM(po.total_with_tax) AS total_purchased,
    AVG(po.total_with_tax) AS avg_ticket,
    SUM(CASE WHEN po.status = 'CLOSED' THEN 1 ELSE 0 END) * 1.0
        / COUNT(*) AS completion_rate
FROM suppliers s
JOIN purchase_orders po ON po.supplier_id = s.id
WHERE po.created_at >= DATEADD(month, -1, GETDATE())
GROUP BY s.id, s.cif, s.name
ORDER BY total_purchased DESC;
```

---

## 📐 Implementación: motor de reportes

### Patrón: Materialized Views vs On-Demand

```
Reportes pre-calculados (materialized views):
  - KPIs ejecutivos (se calculan 1× al día)
  - Top proveedores (se actualiza cada hora)
  - Stock bajo mínimo (se actualiza cada 15 min)

Reportes on-demand:
  - Detalle de PO específica
  - Histórico de un producto
  - Búsqueda de facturas
```

### Caché con Redis

```python
def get_dashboard_data(user_id):
    cache_key = f"dashboard:{user_id}:{today()}"
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # Calcular fresh
    data = {
        "pending_pos": get_pending_pos_count(),
        "open_discrepancies": get_open_discrepancies(),
        "low_stock_items": get_low_stock_items(),
        # ...
    }

    # Cache 5 minutos
    redis.setex(cache_key, 300, json.dumps(data))
    return data
```

---

## 📚 Referencias

- Wikipedia: [Inventory management (business)](https://en.wikipedia.org/wiki/Inventory_management_(business))
- Wikipedia: [Warehouse management system](https://en.wikipedia.org/wiki/Warehouse_management_system)

---

*Siguiente: [13 · Normativa España](./13-normativa-espana.md)*
