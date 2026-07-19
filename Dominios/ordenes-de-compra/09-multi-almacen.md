---
session: ordenes-de-compra
title: "Multi-almacén"
---

# 09 · Multi-almacén

> **Cómo estructurar múltiples warehouses, ubicaciones físicas dentro de cada uno, transferencias internas.**

**Creado:** Julio 2026

---

## 🎯 Por qué importa

Tenés 3 almacenes (Madrid, Barcelona, Sevilla). El stock vive en **3 dimensiones**:

1. **Producto** (qué)
2. **Almacén** (dónde)
3. **Ubicación física dentro del almacén** (dónde exacto)

Y además tenés **estados** del stock (disponible, cuarentena, devolución).

---

## 🗃️ Modelo de datos

### Tabla `Warehouse`

```
Warehouse:
  - id (PK)
  - code (MAD-CEN, BAR-NOR, SEV-SUR)  -- único, kebab-case uppercase
  - name (Madrid Central)
  - address (Calle Logística 123, Madrid)
  - manager_user_id (FK → User)
  - type (CENTRAL, REGIONAL, TRANSIT)
  - timezone (Europe/Madrid)
  - active (bool)
  - created_at
```

### Tabla `WarehouseLocation`

```
WarehouseLocation:
  - id (PK)
  - warehouse_id (FK → Warehouse)
  - code (P3-EB = Pasillo 3, Estantería B)
  - description (Pasillo 3, Estantería B, Nivel 2)
  - type (RECEIVING, STORAGE, PICKING, QUARANTINE, RETURN, DOCK)
  - capacity_units (nullable)
  - active (bool)
```

### Tipos de ubicación

```
RECEIVING    → Muelle de recepción, zona temporal
STORAGE      → Estanterías normales
PICKING      → Zona de preparación de pedidos
QUARANTINE   → Productos dañados o en revisión
RETURN       → Devoluciones a proveedor
DOCK         → Zona de carga/descarga
```

### Tabla `Stock`

```
Stock:
  - id (PK)
  - product_id (FK → Product)
  - warehouse_id (FK → Warehouse)
  - location_id (FK → WarehouseLocation, nullable)
  - quantity (1200)
  - reserved_quantity (0)         -- para ventas pendientes
  - available_quantity (1200)     -- quantity - reserved
  - wac_unit_cost (0.1467)
  - updated_at
```

---

## 🏢 Ejemplo de estructura física

### Madrid Central

```
┌─────────────────────────────────────────────────────────┐
│ ALMACÉN MADRID CENTRAL                                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ MUELLE   │  │ RECEIVING│  │ STORAGE  │  │PICKING ││
│  │  (DOCK)  │─►│  (Z1-R) │─►│ (P1-P10) │─►│ (PI-1) ││
│  └──────────┘  └──────────┘  └──────────┘  └────────┘│
│       │              │             │             │      │
│       │              │             │             ▼      │
│       │              │             │      [Cliente]     │
│       │              │             │                    │
│       │              │      ┌──────────┐  ┌──────────┐  │
│       │              │      │QUARANTINE│  │  RETURN  │  │
│       └──────────────┴─────►│  (Q-1)   │  │  (R-1)   │  │
│                              └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────┘

RECEIVING (Z1-R): Zona temporal donde llega la mercancía
  - Stock aquí cuenta como "recibido" pero no "disponible"
  - Después de validación, se mueve a STORAGE

STORAGE (P1-P10): Pasillos con estanterías
  - Stock disponible para venta
  - Cada SKU tiene una ubicación fija (preferred)

QUARANTINE (Q-1): Productos dañados/pendientes
  - Stock NO disponible para venta
  - Requiere resolución

RETURN (R-1): Devoluciones a proveedor
  - Productos que se devuelven
  - Stock NO disponible

PICKING (PI-1): Zona de preparación
  - Stock reservado para pedidos pendientes
```

---

## 🔄 Flujo de stock por zonas

### Recepción (GR)

```
1. Mercancía llega al MUELLE (DOCK)
2. Ana escanea y confirma GR
3. Sistema crea SLE: +qty en RECEIVING zone
4. Ana valida → mueve stock a STORAGE
5. Sistema crea SLE interno: -qty RECEIVING, +qty STORAGE
6. Stock ahora disponible para venta
```

### Venta

```
1. Cliente pide 50 unidades
2. Sistema busca stock en STORAGE
3. Crea reserva: available -= 50, reserved += 50
4. Operario prepara pedido en PICKING
5. Genera SLE: -qty STORAGE (sale)
6. Reserva se elimina
```

### Devolución de cliente

```
1. Cliente devuelve producto
2. Mercancía llega a RETURN zone
3. Operario valida estado
4. Si OK: SLE interno RETURN → STORAGE (devuelta al stock disponible)
5. Si dañada: SLE interno RETURN → QUARANTINE
```

---

## 🔀 Transferencias entre almacenes

### Caso de uso

```
Madrid tiene 1200 uds de TORN-M8-30-GAL (sobra)
Barcelona tiene 100 uds (falta)

Solución: transferir 500 uds de Madrid a Barcelona
```

### Implementación

```
┌────────────────────────────────────────────────────────┐
│ TRANSFER #TR_2026_0099                                 │
├────────────────────────────────────────────────────────┤
│ Origen:      Madrid Central (almacén + ubicación)      │
│ Destino:     Barcelona Norte (almacén + ubicación)     │
│ Producto:    TORN-M8-30-GAL                            │
│ Cantidad:    500 uds                                   │
│ Transportista: Interno (camión de la empresa)          │
│ Coste transporte: 45€ (asignado a cuenta gastos)       │
│                                                        │
│ Movimientos:                                           │
│  - SLE: Madrid -500 uds @ 0,1467€/u = -73,35€        │
│  - SLE: Barcelona +500 uds @ 0,1467€/u = +73,35€     │
│  - SIN generación de asientos contables               │
│    (es movimiento interno, no compra)                  │
│                                                        │
│ Estados:                                                │
│  - DRAFT → IN_TRANSIT → RECEIVED → COMPLETED          │
└────────────────────────────────────────────────────────┘
```

### Estados de transferencia

```
DRAFT        -- Transferencia creada, no enviada
IN_TRANSIT   -- Salida del origen confirmada
RECEIVED     -- Llegada al destino confirmada
COMPLETED    -- Stock actualizado en destino
CANCELLED    -- Cancelada antes de IN_TRANSIT
```

---

## 📊 Reportes multi-almacén

### Stock por almacén/producto

```
┌──────────────────────────────────────────────────────────┐
│ STOCK DE TORN-M8-30-GAL                                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ Por almacén:                                             │
│   Madrid Central:     1.200 uds @ 0,1467€ = 176,00€   │
│   Barcelona Norte:      800 uds @ 0,1500€ = 120,00€   │
│   Sevilla Sur:          400 uds @ 0,1480€ =  59,20€   │
│   ─────────────────────────────────────────────         │
│   TOTAL:              2.400 uds            = 355,20€   │
│                                                          │
│ Por ubicación dentro de Madrid:                          │
│   P3-EB (Storage):     1.000 uds @ 0,1467€             │
│   P5-EC (Storage):       200 uds @ 0,1450€             │
│   PI-1 (Picking):          0 uds (todo reservado)      │
│   Q-1 (Quarantine):        0 uds                        │
│   ─────────────────────────────────────────             │
│   TOTAL Madrid:        1.200 uds @ 0,1467€ = 176,00€  │
└──────────────────────────────────────────────────────────┘
```

### KPIs operativos por almacén

```
┌──────────────────────────────────────────────────────────┐
│ DASHBOARD ALMACÉN MADRID — Julio 2026                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ Valor stock:              45.678,32€                    │
│ Items en stock:            1.234                        │
│ Ubicaciones activas:         87                         │
│                                                          │
│ Rotación stock (DSI):       18 días                     │
│ Exactitud inventario:      99,2%                        │
│ Recepciones pendientes:       1                         │
│ Transferencias en tránsito:   2                         │
│                                                          │
│ Top 5 SKUs por valor:                                   │
│   1. TORN-M8-30-GAL         176,00€ (38%)              │
│   2. TUE-10-AZUL            145,00€ (31%)              │
│   3. ARAN-M8-30-GAL          89,00€ (19%)              │
│   4. TORN-M6-20-GAL          65,00€ (14%)              │
│   5. Otros                  180,32€ (39%)              │
└──────────────────────────────────────────────────────────┘
```

---

## ⚠️ Casos edge

### Stock negativo por error

```
Si por race condition dos procesos decrementan simultáneamente:
  - Bloquear con SELECT FOR UPDATE en transacciones
  - O usar optimistic locking con version
  - O usar Redis/DB advisory locks
```

### Producto en múltiples ubicaciones del mismo almacén

```
TORN-M8-30-GAL está en:
  - P3-EB: 1000 uds
  - P5-EC:  200 uds

Al vender:
  - Sistema toma de P3-EB primero (ubicación preferente)
  - O usa FIFO/LIFO de ubicaciones
  - O el operario elige manualmente
```

### Transferencia entre almacenes de distinta empresa

```
Caso raro: si tu CRM maneja múltiples empresas (multi-tenant)

  Empresa A (Madrid) → Empresa B (Barcelona)
  
  Esto NO es transferencia interna
  Es una venta entre empresas
  Genera factura + IVA + asientos contables en ambas
```

---

## 📐 Implementación algorítmica

### Pseudocódigo: receive stock

```
function receive_stock(gr_id, product_id, qty, warehouse_id, location_id):
    # 1. Crear SLE en zona RECEIVING
    create_sle({
        product_id: product_id,
        warehouse_id: warehouse_id,
        location_id: receiving_zone(warehouse_id),
        qty_change: qty,
        value_change: qty * provisional_price,
        provisional: true,
        source_type: 'GR',
        source_id: gr_id
    })

    # 2. Stock NO disponible aún (sigue en RECEIVING)
    update_stock(product_id, warehouse_id, location=receiving_zone, quantity+=qty)

function move_stock(product_id, from_location, to_location, qty):
    # Mover entre zonas (sin SLE contable, solo cambio de ubicación)
    from_stock = get_stock(product_id, from_location)
    to_stock = get_stock(product_id, to_location)

    from_stock.quantity -= qty
    to_stock.quantity += qty

    if to_location.type == 'STORAGE':
        # Ahora disponible para venta
        to_stock.available_quantity = to_stock.quantity
```

### Pseudocódigo: transfer between warehouses

```
function transfer_stock(transfer_id):
    if transfer.status == 'IN_TRANSIT':
        # Confirmar salida
        from_stock = get_stock(transfer.product_id, transfer.from_warehouse)
        from_stock.quantity -= transfer.quantity
        from_stock.available_quantity -= transfer.quantity
        # SLE negativo en origen
        create_sle({
            product_id: transfer.product_id,
            warehouse_id: transfer.from_warehouse,
            qty_change: -transfer.quantity,
            value_change: -transfer.quantity * from_stock.wac,
            source_type: 'TRANSFER',
            source_id: transfer_id
        })

    elif transfer.status == 'RECEIVED':
        # Confirmar llegada
        to_stock = get_stock(transfer.product_id, transfer.to_warehouse)
        to_stock.quantity += transfer.quantity
        to_stock.available_quantity += transfer.quantity
        # SLE positivo en destino (mismo precio WAC del origen)
        create_sle({
            product_id: transfer.product_id,
            warehouse_id: transfer.to_warehouse,
            qty_change: transfer.quantity,
            value_change: transfer.quantity * transfer.wac_at_origin,
            source_type: 'TRANSFER',
            source_id: transfer_id
        })
```

---

## 📚 Referencias

- Wikipedia: [Warehouse management system](https://en.wikipedia.org/wiki/Warehouse_management_system)
- Wikipedia: [Inventory management (business)](https://en.wikipedia.org/wiki/Inventory_management_(business))

---

*Siguiente: [10 · Tolerancia de discrepancia <2%](./10-tolerancia-discrepancia.md)*
