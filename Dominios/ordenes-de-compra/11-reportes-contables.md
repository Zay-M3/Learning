---
session: ordenes-de-compra
title: "Reportes contables (PGC España)"
---

# 11 · Reportes contables (PGC España)

> **Qué libros y reportes necesita un contable en España** cuando tiene un CRM con módulo de compras. Asientos, libros oficiales, IVA.

**Creado:** Julio 2026

---

## 🎯 El PGC y tu CRM

El **Plan General Contable (PGC)** español es la normativa que define cómo se contabilizan las operaciones. Tu CRM NO es un software contable, pero debe **generar los asientos contables** que el contable (Laura) revisará y pasará al programa contable oficial (A3, Sage, etc.).

---

## 📚 Cuentas PGC clave para compras

### Grupo 3: Existencias (Stock)

```
300  Mercaderías                          -- Stock de productos para venta
301  Materias primas                      -- Stock para producción
302  Otros aprovisionamientos             -- Materiales consumibles
390  Provisión depreciación existencias   -- Si hay mermas/pérdidas
```

### Grupo 4: Acreedores y deudores por operaciones de tráfico

```
400  Proveedores                          -- Deuda con proveedores (corto plazo)
401  Proveedores, efectos comerciales a pagar
410  Acreedores por prestaciones de servicios
472  H.P. IVA soportado                   -- IVA que recuperamos
477  H.P. IVA repercutido                 -- IVA que cobramos
```

### Grupo 6: Compras y gastos por naturaleza

```
600  Compras de mercaderías               -- Compra de productos para venta
602  Compras de otros aprovisionamientos
608  Devoluciones de compras              -- Notas de crédito recibidas
609  Rappels por compras                  -- Descuentos por volumen/pronto pago
```

### Grupo 7: Ventas e ingresos (cubre variances)

```
700  Ventas de mercaderías
708  Devoluciones de ventas
709  Rappels sobre ventas
798  Diferencias de precio en compras     -- PPV: variance entre PO e invoice
```

---

## 📋 Reportes contables obligatorios para España

### 1. Libro Diario (asientos cronológicos)

```
┌──────────────────────────────────────────────────────────────┐
│ LIBRO DIARIO — Julio 2026                                    │
├──────────────────────────────────────────────────────────────┤
│ #1  2026-07-01  Compra tornillería García - PO_2026_0042     │
│ #2  2026-07-15  Aprobación PO_2026_0042                      │
│ #3  2026-07-18  Recepción mercancía - GR_2026_0042          │
│ #4  2026-07-19  Factura GARCIA-FAC-2026-1523               │
│ #5  2026-07-19  Ajuste stock por invoice real               │
│ #6  2026-07-20  Venta a cliente XYZ                        │
│ #7  2026-07-25  Pago a García                             │
└──────────────────────────────────────────────────────────────┘

Cada asiento debe tener:
  - Fecha
  - Número correlativo (sin saltos)
  - Descripción
  - Cuentas DEBE / HABER con importes
  - Documento soporte (PO, GR, Factura)
```

### 2. Libro Mayor (movimientos por cuenta)

```
┌──────────────────────────────────────────────────────────────┐
│ CUENTA 400 — Proveedores (García)                            │
├──────────────────────────────────────────────────────────────┤
│ Fecha      │ Concepto              │ Debe    │ Haber   │ Saldo│
├──────────────────────────────────────────────────────────────┤
│ 2026-07-01 │ Saldo inicial         │         │         │   0  │
│ 2026-07-19 │ Factura GARCIA-FAC... │         │ 175,50  │175,50│
│ 2026-07-25 │ Pago transferencia   │ 175,50  │         │   0  │
│ 2026-07-31 │ Saldo final           │         │         │   0  │
└──────────────────────────────────────────────────────────────┘
```

### 3. Libro de IVA soportado

```
┌──────────────────────────────────────────────────────────────┐
│ LIBRO IVA SOPORTADO — Julio 2026 (TRIMESTRAL)                │
├──────────────────────────────────────────────────────────────┤
│ Factura        │ Proveedor   │ Fecha     │ Base  │ IVA 21% │
├──────────────────────────────────────────────────────────────┤
│ GARCIA-FAC-... │ García      │ 2026-07-19│ 145,04│ 30,46  │
│ SUR-FAC-...    │ Sur         │ 2026-07-22│ 250,00│ 52,50  │
│ NORTE-FAC-...  │ Norte       │ 2026-07-25│ 180,00│ 37,80  │
├──────────────────────────────────────────────────────────────┤
│ TOTAL          │             │           │ 575,04│ 120,76 │
└──────────────────────────────────────────────────────────────┘

→ Para declaración trimestral de IVA (modelo 303)
```

### 4. Balance de Sumas y Saldos

```
┌──────────────────────────────────────────────────────────────┐
│ BALANCE DE SUMAS Y SALDOS — 2026-07-31                       │
├──────────────────────────────────────────────────────────────┤
│ Cuenta │ Nombre              │ Suma Debe │ Suma Haber │ Saldo│
├──────────────────────────────────────────────────────────────┤
│ 300    │ Mercaderías         │  178,00   │     2,00   │176,00│
│ 400    │ Proveedores         │  175,50   │   175,50   │  0,00│
│ 472    │ H.P. IVA soportado  │   30,46   │     0,00   │ 30,46│
│ 600    │ Compras mercaderías │  148,00   │   148,00   │  0,00│
│ 609    │ Rappels por compras │    2,96   │     0,00   │  2,96│
│ 798    │ Dif. precio compras │    2,00   │     0,00   │  2,00│
└──────────────────────────────────────────────────────────────┘

→ Para cierre contable mensual/anual
```

### 5. Cuenta de Pérdidas y Ganancias

```
┌──────────────────────────────────────────────────────────────┐
│ PYG — Julio 2026                                             │
├──────────────────────────────────────────────────────────────┤
│ INGRESOS                                                    │
│   700  Ventas                       12.500,00               │
│                                                              │
│ GASTOS                                                      │
│   600  Compras mercaderías            148,00               │
│   798  Dif. precio compras              2,00               │
│   (606) Servicios bancarios           45,00               │
│   (628) Suministros                  120,00               │
│                                                              │
│ RESULTADO DEL MES:           12.183,00 (positivo)          │
└──────────────────────────────────────────────────────────────┘

⚠️ El ajuste de stock (variación de existencias) se hace
   automáticamente: existencias_iniciales - existencias_finales
   = CMV (coste de mercaderías vendidas)
```

### 6. Diferencias de precio (cuenta 798)

```
┌──────────────────────────────────────────────────────────────┐
│ DIFERENCIAS DE PRECIO EN COMPRAS — Julio 2026               │
├──────────────────────────────────────────────────────────────┤
│ PO         │ Proveedor  │ Precio PO │ Precio Fact │ Variance│
├──────────────────────────────────────────────────────────────┤
│ PO_0042    │ García     │ 150,00    │ 148,00      │  -2,00  │
│ PO_0051    │ Sur        │ 280,00    │ 280,00      │   0,00  │
│ PO_0063    │ Norte      │ 200,00    │ 210,00      │ +10,00  │
├──────────────────────────────────────────────────────────────┤
│ TOTAL FAVORABLE:                          -2,00             │
│ TOTAL DESFAVORABLE:                      +10,00             │
│ NETO:                                     +8,00             │
└──────────────────────────────────────────────────────────────┘

→ Para auditoría interna
→ Para análisis de savings vs presupuesto
```

---

## 🧾 Asientos típicos del flujo P2P

### Asiento 1: Aprobación de PO (NO genera asiento contable)

```
Solo marca el PO como APPROVED en el sistema.
NO hay movimiento contable hasta que llegue la mercancía.
```

### Asiento 2: Recepción de mercancía (GR)

```
NO genera asiento contable aún.
Solo crea SLE (Stock Ledger Entry) con valoración provisional.

Pero SÍ crea el "compromiso" en sistema de presupuesto.
```

### Asiento 3: Factura del proveedor (Invoice)

```
┌─────────────────────────────────────────────────────────────┐
│ ASIENTO #2026-07-19-0042                                    │
│ Fecha: 2026-07-19                                           │
│ Concepto: Fra. GARCIA-FAC-2026-1523 - Tornillería          │
├─────────────────────────────────────────────────────────────┤
│ DEBE:                                                       │
│   600. Compras de mercaderías           148,00€             │
│   472. H.P. IVA soportado               30,46€             │
│                                                            │
│ HABER:                                                      │
│   400. Proveedores                     175,50€             │
│   609. Rappels por compras               -2,96€            │
│                                                            │
│ Documento soporte: Fra. GARCIA-FAC-2026-1523                │
└─────────────────────────────────────────────────────────────┘
```

### Asiento 4: Ajuste de stock (variance)

```
┌─────────────────────────────────────────────────────────────┐
│ ASIENTO #2026-07-19-0043 (complementario)                   │
│ Concepto: Ajuste precio stock PO_2026_0042                  │
├─────────────────────────────────────────────────────────────┤
│ DEBE:                                                       │
│   300. Mercaderías                     -2,00€              │
│                                                            │
│ HABER:                                                      │
│   798. Diferencias de precio en compras -2,00€              │
│                                                            │
│ (Reduce stock porque precio real fue menor al provisional)  │
└─────────────────────────────────────────────────────────────┘
```

### Asiento 5: Pago al proveedor

```
┌─────────────────────────────────────────────────────────────┐
│ ASIENTO #2026-07-25-0010                                    │
│ Concepto: Pago Fra. GARCIA-FAC-2026-1523                   │
├─────────────────────────────────────────────────────────────┤
│ DEBE:                                                       │
│   400. Proveedores                     175,50€             │
│                                                            │
│ HABER:                                                      │
│   572. Bancos c/c                       175,50€             │
│                                                            │
│ Documento soporte: Orden de transferencia #TR-2026-7891     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Exportes a programas contables

Tu CRM debe poder **exportar asientos** en formatos que los programas contables españoles entiendan:

### Formato A3 (A3 Software)

```
CSV con estructura específica:
  fecha|asiento|descripcion|cuenta_debe|cuenta_haber|importe|debe_haber|documento
```

### Formato Sage Despachos

```
XML con schema propio de Sage
```

### Formato genérico (CSV/Excel)

```
Cualquier programa contable puede importar CSV básico:
  fecha, cuenta, importe, debe_haber, concepto, documento
```

### Conexión API

```
Programas modernos (Holded, Quipu, etc.) tienen APIs REST:
  POST /v1/accounting/entries
  {
    "date": "2026-07-19",
    "description": "Fra. GARCIA-FAC-2026-1523",
    "lines": [
      {"account": "600", "debit": 148.00},
      {"account": "472", "debit": 30.46},
      {"account": "400", "credit": 175.50},
      {"account": "609", "credit": -2.96}
    ]
  }
```

---

## 🇪🇸 Específico España: SII, IVA, IRPF

### Tipos de IVA en España

```
General:        21%  (tornillería, electrónica, ropa)
Reducido:       10%  (alimentación, libros, transporte)
Superreducido:   4%  (pan, leche, libros básicos, vivienda)
Exento:          0%  (Canarias, Ceuta, Melilla, operaciones exentas)
```

### Inversión del sujeto pasivo

```
Cuando el proveedor es extracomunitario (fuera de UE):
  - IVA no se aplica en factura del proveedor
  - El comprador (vos) autoliquida IVA
  - Asiento diferente:
    DEBE: 600 Compras (sin IVA)
    DEBE: 472 IVA soportado (autoliquidado)
    HABER: 400 Proveedores
```

### Recargo de equivalencia

```
Si comprás a proveedor que está en régimen de recargo:
  - Aplica recargo adicional sobre IVA
  - Ej: IVA 21% + RE 5,2% = 26,2% total
  - Asiento adicional en cuenta 472.REC
```

### Retención IRPF (profesionales)

```
Si el proveedor es profesional (no empresa):
  - Retención 15% (o 7% nuevos profesionales)
  - El proveedor NO cobra el IRPF, lo retiene el cliente
  - Asiento:
    DEBE: 600/628 Compras/Gastos (importe total)
    HABER: 400 Proveedores (importe - retención)
    HABER: 4751 H.P. Acreedor por retenciones (importe retenido)
```

### SII (Suministro Inmediato de Información)

> Fuente: [AEAT SII](https://www.agenciatributaria.es/)

```
Sistema de envío de libros registro IVA en tiempo real (4 días).

Aplica a:
  - Empresas con volumen > 6M€ facturación
  - Inscritas en REDEME (Registro de Devolución Mensual del IVA)
  - Grupos de IVA

Tu CRM NO envía al SII directamente, pero debe:
  - Marcar facturas como "SII ready"
  - Generar el XML con estructura AEAT
  - Permitir descarga para envío manual o integración
```

---

## 📐 Implementación: motor de asientos

### Tabla `AccountingEntry`

```
AccountingEntry:
  - id (PK)
  - entry_number (correlativo)
  - date
  - description
  - source_type ('INVOICE' | 'PAYMENT' | 'ADJUSTMENT' | etc.)
  - source_id (id del documento origen)
  - company_id (multi-tenant)
  - lines: list of AccountingEntryLine
```

### Tabla `AccountingEntryLine`

```
AccountingEntryLine:
  - id (PK)
  - entry_id (FK)
  - account_code (600, 472, 400, etc.)
  - debit (importe DEBE)
  - credit (importe HABER)
  - description
  - dimensions: dict (centro de costo, proyecto, etc.)
```

### Pseudocódigo: generar asiento desde invoice

```
function generate_entry_from_invoice(invoice):
    lines = []

    # Línea 1: Compra
    lines.append({
        account_code: '600',
        debit: invoice.subtotal,
        credit: 0
    })

    # Línea 2: IVA soportado
    lines.append({
        account_code: '472',
        debit: invoice.tax_amount,
        credit: 0
    })

    # Línea 3: Proveedor (todo el total)
    lines.append({
        account_code: '400',
        debit: 0,
        credit: invoice.total
    })

    # Línea 4: Rappels (si hay descuento)
    if invoice.discount > 0:
        lines.append({
            account_code: '609',
            debit: 0,
            credit: invoice.discount
        })

    # Línea 5: PPV (si hay variance vs PO)
    if invoice.ppv != 0:
        # Ajuste de stock
        lines.append({
            account_code: '300',
            debit: invoice.ppv if invoice.ppv < 0 else 0,
            credit: -invoice.ppv if invoice.ppv > 0 else 0
        })
        lines.append({
            account_code: '798',
            debit: -invoice.ppv if invoice.ppv < 0 else 0,
            credit: invoice.ppv if invoice.ppv > 0 else 0
        })

    entry = create_accounting_entry(
        date=invoice.date,
        description=f"Fra. {invoice.number} - {invoice.supplier.name}",
        source_type='INVOICE',
        source_id=invoice.id,
        lines=lines
    )

    return entry
```

---

## 📚 Referencias

- Wikipedia: [Factura electrónica en España](https://es.wikipedia.org/wiki/Factura_electr%C3%B3nica_en_Espa%C3%B1a)
- AEAT: [Suministro Inmediato de Información](https://www.agenciatributaria.es/)
- Gobierno de España: [Facturae](https://www.facturae.gob.es/)

---

*Siguiente: [12 · Reportes operativos](./12-reportes-operativos.md)*
