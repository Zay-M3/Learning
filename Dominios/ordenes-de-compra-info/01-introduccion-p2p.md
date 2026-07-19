---
session: Dominios
title: "Introducción al ciclo Purchase-to-Pay (P2P)"
---

# 01 · Introducción al ciclo Purchase-to-Pay (P2P)

> **Qué es P2P, por qué existe, qué vocabulario usaremos en el resto de la documentación.**

**Creado:** Julio 2026

---

## 📖 Definición formal

**Purchase-to-Pay (P2P)**, también llamado **Procure-to-Pay** y coloquialmente **req to check**, se refiere a los procesos de negocio que cubren las actividades de:

```
1. Solicitar (requisitioning)
2. Comprar
3. Recibir
4. Pagar
5. Contabilizar
```

para bienes y servicios.

> *"Most organisations have a formal process and specialist staff to control this activity so that spending is not wasteful or fraudulent."*
> — Fuente: [Wikipedia · Purchase-to-pay](https://en.wikipedia.org/wiki/Purchase-to-pay)

---

## 🎯 Por qué existe este proceso

El P2P existe por **3 razones estratégicas**:

| Razón | Qué cubre | Quién lo necesita |
|-------|-----------|-------------------|
| **Control de gasto** | Saber qué se compra, a quién, por cuánto | Dirección financiera |
| **Prevención de fraude** | Evitar pagos a proveedores inexistentes / inflados | Auditoría interna |
| **Trazabilidad legal** | Cumplir normativa contable y fiscal | Asesoría fiscal / AEAT |

---

## 📚 Vocabulario canónico (usado en toda esta documentación)

| Término inglés | Español | Abrev. | Definición |
|----------------|---------|--------|------------|
| **Purchase Order** | Orden de compra | PO | Documento comercial emitido por comprador a vendedor |
| **Goods Receipt** | Recepción de mercancía | GR / GRN | Documento que valida qué se recibió físicamente |
| **Goods Received Note** | Nota de recepción | GRN | Sinónimo de GR (más usado en UK) |
| **Purchase Invoice** | Factura de proveedor | PI | Documento fiscal que cobra el proveedor |
| **Vendor Bill** | Factura de proveedor | VB | Sinónimo americano de PI |
| **Vendor** | Proveedor | — | Quien vende |
| **Supplier** | Proveedor | — | Sinónimo de vendor |
| **Three-Way Matching** | Validación de 3 documentos | 3WM | PO ↔ GR ↔ Invoice |
| **Stock Ledger Entry** | Apunte de stock | SLE | Cada movimiento individual de stock |
| **Valuation Rate** | Tasa de valoración | VR | Costo unitario del stock |
| **Landed Cost** | Costo en destino | LC | Costos adicionales (flete, aduana) |
| **Landed Cost Voucher** | Asiento de costo en destino | LCV | Documento que aplica LC al stock |
| **Stock Reconciliation** | Reconciliación de stock | SR | Ajuste físico vs sistema |
| **Purchase Price Variance** | Variación de precio de compra | PPV | Diferencia PO vs factura real |

---

## 🗺️ Mapa de los 15 markdowns

```
01. ESTÁS AQUÍ — Introducción P2P
    │
    ├─ 02. Flujo completo (walkthrough)
    │   └─ Diagrama general + ejemplo numérico paso a paso
    │
    ├─ 03. Three-Way Matching
    │   └─ El control antifraude clásico (1-way / 2-way / 3-way / 4-way)
    │
    ├─ 04. Estados de la PO
    │   └─ Lifecycle completo (Draft → Closed)
    │
    ├─ 05. Estrategias de actualización de stock
    │   └─ On Receipt vs On Invoice vs Provisional+Adjust vs Continuous
    │
    ├─ 06. Métodos de valoración de inventario
    │   └─ FIFO / LIFO / WAC / Standard
    │
    ├─ 07. Formatos de exportación
    │   └─ PDF / XLSX / CSV / XML / UBL / PEPPOL / Facturae
    │
    ├─ 08. Multi-proveedor con variantes de precio
    │   └─ Mismo producto, distintos precios
    │
    ├─ 09. Multi-almacén
    │   └─ Estructura de warehouses + ubicaciones + transferencias
    │
    ├─ 10. Tolerancia de discrepancia <2%
    │   └─ Cálculo + edge cases + recomendación
    │
    ├─ 11. Reportes contables
    │   └─ PGC España + libros obligatorios
    │
    ├─ 12. Reportes operativos
    │   └─ KPIs + dashboards
    │
    ├─ 13. Normativa España
    │   └─ Ley Crea y Crece / VeriFactu / TicketBAI / SII / Facturae
    │
    ├─ 14. Decisiones de arquitectura pendientes
    │   └─ 8 decisiones críticas antes de codear
    │
    └─ 15. Bibliografía
        └─ Links oficiales verificados
```

---

## 🚦 Estado de la documentación

```
[✓] Investigación completa
[ ] PRD (Product Requirements Document)
[ ] Diseño técnico (modelo de BD, APIs, etc.)
[ ] Implementación
[ ] Tests
[ ] Deploy
```

---

## 🎓 Cómo aprovechar esta documentación

1. **Antes de implementar:** leer del 01 al 14 completo. Te dará el modelo mental completo del dominio.
2. **Durante implementación:** tener abierto como referencia. Especialmente 02 (walkthrough), 05 (stock strategies), 06 (valoración), 13 (normativa España).
3. **Para decisiones puntuales:** saltar al markdown específico según la duda.
4. **Para auditoría:** la sección de bibliografía (15) tiene todas las fuentes oficiales que validan cada afirmación.

---

*Siguiente: [02 · Flujo completo paso a paso](./02-flujo-completo.md)*
