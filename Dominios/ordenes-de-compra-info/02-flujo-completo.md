# 02 · Flujo completo P2P paso a paso

> **Walkthrough con ejemplo numérico completo**, desde que Carlos crea la PO hasta que Laura contabiliza la factura.

**Creado:** Julio 2026

---

## 🎬 El escenario de ejemplo (lo seguimos durante todo el documento)

```
Empresa:        "Logística Martín S.L." (CIF B-12345678)
Producto:       Tornillo M8x30 galvanizado (SKU: TORN-M8-30-GAL)
Proveedor A:    "Suministros García" (CIF B-87654321) → 0,15€/ud
Proveedor B:    "Metalúrgica Sur"   (CIF B-11223344) → 0,18€/ud
Almacenes:      3 (Madrid Central, Barcelona Norte, Sevilla Sur)
Operador:       Ana (recepción en Madrid)
Aprobador:      Carlos (compras)
Contable:       Laura (financiero)
```

---

## 🔄 Diagrama general del flujo

```
    ┌──────────────┐                                          ┌──────────────┐
    │  COMPRAS     │──── 1. Crear PO ─────►                   │  PROVEEDOR   │
    │  (Carlos)    │──── 2. Aprobar PO ──►                   │  (García)    │
    │              │──── 3. Enviar PO ────► PO_2026_0042.pdf   │              │
    └──────────────┘                                          └──────┬───────┘
                                                                       │
                                          (días/semanas después)       │
                                                                       ▼
    ┌──────────────┐                                          ┌──────────────┐
    │  ALMACÉN     │◄── 4. Llega mercancía ──────────────────│  TRANSPORTE  │
    │  (Ana)       │                                          │              │
    │  Madrid      │                                          └──────────────┘
    │              │
    │              │──── 5. Verificar GR contra PO
    │              │──── 6. Validar cantidades/estado
    │              │──── 7. Reportar discrepancias (si las hay)
    └──────┬───────┘
           │
           │ Si OK (3-way provisional)
           ▼
    ┌──────────────┐
    │  SISTEMA     │──── 8. Actualizar stock (provisional con precio PO)
    │  (CRM)       │──── 9. Registrar GR en log
    └──────┬───────┘
           │
           │ (días/semanas después)
           ▼
    ┌──────────────┐
    │  PROVEEDOR   │──── 10. Envía factura electrónica ──►
    │              │       Facturae XML + PDF
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  CONTABLE    │──── 11. Recibe factura
    │  (Laura)     │──── 12. Valida 3-way (PO+GR+Invoice)
    │              │──── 13. Calcula price variance
    │              │──── 14. Ajusta stock valuation
    │              │──── 15. Genera asiento contable
    │              │──── 16. Reporta a SII/VeriFactu (si aplica)
    └──────┬───────┘
           │
           │ Si todo OK
           ▼
    ┌──────────────┐
    │  TESORERÍA   │──── 17. Programa pago al proveedor
    └──────────────┘
```

---

## 🚶 Walkthrough de los 14 pasos

### PASO 1: Crear la Orden de Compra (Borrador)

**Actor:** Carlos (Compras)

**Acción:** Carlos detecta que el stock de TORN-M8-30-GAL en Madrid está bajo. Abre el módulo de compras del CRM y crea una nueva PO.

```
┌──────────────────────────────────────────────────┐
│ PO #PO_2026_0042                                 │
│ Estado: DRAFT (Borrador)                         │
│ Proveedor: Suministros García (B-87654321)       │
│ Almacén destino: Madrid Central                  │
│ Fecha esperada entrega: 2026-07-25               │
│ Solicitante: Carlos Martín                       │
│                                                  │
│ Líneas:                                          │
│ ┌──────────────────────────────────────────┐    │
│ │ SKU           │ Cant │ Precio/u │ Total  │    │
│ ├──────────────────────────────────────────┤    │
│ │ TORN-M8-30-GAL│1000  │ 0,15€    │ 150,00€│    │
│ │              IVA 21% │         │  31,50€│    │
│ │              TOTAL   │         │ 181,50€│    │
│ └──────────────────────────────────────────┘    │
└──────────────────────────────────────────────────┘
```

**Estados del documento:**
- ✅ Creado en BD (pero NO afecta stock aún)
- ✅ Numeración interna (PO_2026_0042) generada
- ✅ Línea de producto vinculada al maestro
- ❌ Stock NO modificado
- ❌ Sin valor contable

**Validaciones automáticas del sistema:**
- ¿Proveedor existe? ✅ García existe y está activo
- ¿Producto existe? ✅ TORN-M8-30-GAL existe en maestro
- ¿Almacén destino existe? ✅ Madrid Central
- ¿Precio coherente con histórico? ⚠️ (último 0,14€, ahora 0,15€ — +7% — flag amarillo)
- ¿Stock actual del almacén? ✅ 200 uds (por debajo del mínimo de 500)

---

### PASO 2: Aprobar la PO internamente

**Actor:** Carlos (o un aprobador delegado)

**Acción:** Carlos revisa los detalles. Click en "Aprobar".

```
Cambio de estado: DRAFT → APPROVED

Eventos disparados:
  - Timestamp: approved_at = 2026-07-15 10:30
  - Usuario: carlos.martin
  - Log entry: "PO_2026_0042 approved by carlos.martin"

Permisos verificados:
  ✅ Carlos tiene rol "Comprador" + "Aprobador nivel 1" (< 5000€)
  ✅ PO es de 181,50€ → aprobada automáticamente sin escalado
```

**Reglas de aprobación por industria:**

| Monto PO | Aprobador requerido |
|----------|---------------------|
| < 1.000€ | Nivel 1 (Comprador) |
| 1.000€ - 10.000€ | Nivel 2 (Manager) |
| 10.000€ - 50.000€ | Nivel 3 (Director) |
| > 50.000€ | Nivel 4 (Consejo/Dirección General) |

---

### PASO 3: Enviar la PO al proveedor

**Actor:** Sistema (envío automático) o Carlos (manual)

**Acción:** Carlos selecciona formato de exportación. García históricamente prefiere PDF por email.

```
Generación:
  - Plantilla PDF estándar con logo + CIF + datos fiscales
  - Numeración visible: PO_2026_0042
  - Fecha emisión, fecha esperada entrega
  - Términos de pago: 30 días (configurado por defecto para García)
  - IBAN: ya precargado del maestro de proveedores
  - Desglose IVA (21% por defecto en España para tornillería industrial)

Estados:
  DRAFT → APPROVED → SENT
  sent_at: 2026-07-15 10:35
  sent_via: email
  sent_to: pedidos@garcia-suministros.es

Documentos generados:
  - PO_2026_0042.pdf (enviado)
  - log_audit: registro inmutable
```

**Formatos que el CRM debe generar (MVP España):**

```
┌─────────────────────────────────────────────────────────────┐
│ FORMATOS PARA MVP                                           │
├─────────────────────────────────────────────────────────────┤
│ 1. PDF  → 95% de proveedores (visual, firmado)             │
│ 2. XLSX → 40% (editable, permite líneas custom)             │
│ 3. CSV  → 20% (integraciones técnicas simples)              │
│ 4. XML  → 10% (EDI básico)                                  │
│ 5. Facturae → 5% (estándar español, sector público)         │
│ 6. UBL  → futuro (europeo, si escalas a otros mercados)    │
└─────────────────────────────────────────────────────────────┘
```

---

### PASO 4: El proveedor envía la mercancía (mundo real)

```
Acción externa: García prepara el pedido en su almacén.
Acción externa: Transpaleta / camión sale del almacén de García.
Acción externa: Mercancía llega al muelle de Madrid Central.
               (Bultos: 2 cajas, 25 kg cada una, ref "GARCIA-2026-7891")
```

En este punto, **tu CRM no recibe nada todavía**. La mercancía está físicamente en tu almacén pero el sistema no lo sabe.

---

### PASO 5: Recepción de mercancía — Goods Receipt (GR)

**Actor:** Ana (Operaria de almacén)

```
Acción: Ana abre el módulo de "Recepciones" en el CRM.
Acción: Selecciona "Nueva Recepción"
Acción: El sistema le pide vincular a una PO existente.

Ana escanea el código de barras del albarán de García:
  → "GARCIA-2026-7891"
  → Sistema busca la PO asociada
```

**Métodos de vinculación GR ↔ PO:**

| Método | Pros | Contras |
|--------|------|---------|
| A) Selección manual desde dropdown | Simple | Propenso a error humano |
| B) Escaneo código del albarán | El proveedor pone el número de PO | Requiere disciplina del proveedor |
| C) Escaneo QR con la PO | Más robusto | Requiere acuerdo con proveedor |
| D) Sugerencia automática basada en proveedor+SKU | Balance perfecto | Lógica más compleja |

**Recomendación:** empezar con A) y evolucionar a D).

```
Ana selecciona PO_2026_0042. Sistema carga:
  - 1 línea de producto esperada: TORN-M8-30-GAL x 1000
  - Precio acordado: 0,15€/ud
  - Almacén: Madrid Central
  - Proveedor: García
```

---

### PASO 6: Verificación física línea por línea

**Actor:** Ana

```
El sistema le muestra una interfaz de validación:

┌────────────────────────────────────────────────────────────┐
│ RECEPCIÓN DE MERCANCÍA - PO_2026_0042                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ Línea 1: TORN-M8-30-GAL                                    │
│ ┌────────────────────────────────────────────────────┐    │
│ │ Cantidad esperada: 1.000                           │    │
│ │ Cantidad recibida: [____]                          │    │
│ │                                                    │    │
│ │ Estado del producto:                               │    │
│ │  [✓] Aceptado                                      │    │
│ │  [ ] Dañado                                        │    │
│ │  [ ] Cantidad incorrecta                           │    │
│ │  [ ] Producto incorrecto                           │    │
│ │  [ ] Otros (abrir comentario)                      │    │
│ │                                                    │    │
│ │ Almacén de destino: Madrid Central [▼]             │    │
│ │ Ubicación física:   Pasillo 3, Estantería B [▼]    │    │
│ │ Lote (opcional):    LOTE-2026-7891                │    │
│ │ Fecha caducidad:    N/A                            │    │
│ │                                                    │    │
│ │ Comentarios: [_________________________________]   │    │
│ └────────────────────────────────────────────────────┘    │
│                                                            │
│ [Añadir foto evidencia]  [Marcar incidencia]               │
└────────────────────────────────────────────────────────────┘

Ana cuenta la mercancía y reporta:
  Cantidad recibida: 1.000 (todo OK)
  Estado: Aceptado
  Almacén: Madrid Central, Pasillo 3, Estantería B
```

**Ana hace 3 validaciones simultáneas:**

```
1. ¿Cantidad esperada = cantidad recibida?
   Esperado: 1000 → Recibido: 1000 → ✅ OK

2. ¿Producto físico = producto de la línea?
   Lo que llegó: Tornillo M8x30 galvanizado → SKU: TORN-M8-30-GAL → ✅ OK

3. ¿Estado físico = estado aceptable?
   Sin daños visibles → ✅ OK
```

---

### PASO 7: Manejo de discrepancias (qué pasa si algo falla)

#### Caso A: Short-receipt (recibir menos)

```
Esperado: 1000 → Recibido: 980

Ana marca:
  ☑ Cantidad incorrecta (faltan 20 unidades)

Opciones del sistema:
  1. Aceptar parcial: GR con 980, PO con 20 pendientes
  2. Rechazar todo: no crear GR, devolver
  3. Esperar: pausar GR, esperar reposición
```

#### Caso B: Over-receipt (recibir más)

```
Esperado: 1000 → Recibido: 1020

⚠️ OVER-RECEIPT ES RIESGO DE FRAUDE / ERROR ADMINISTRATIVO

Reglas con tolerancia <2%:
  Diferencia <2%: aceptar automáticamente con flag
  Diferencia 2-10%: requiere aprobación del manager
  Diferencia >10%: BLOQUEO total, escalado a dirección
```

#### Caso C: Producto dañado

```
Cantidad OK pero 50 unidades con caja rota

Ana marca:
  ☑ Dañado (50 unidades)

Manejo:
  - Crear GR parcial: 950 aceptadas + 50 en cuarentena
  - Las 50 van al "Almacén Dañados" (cuarentena)
  - Notificación automática al proveedor
  - Claim/RMA generado
  - Stock NO actualizado para las 50 dañadas
```

#### Caso D: Producto equivocado

```
Esperaba TORN-M8-30-GAL, llegó TORN-M8-30-INOX

Ana marca:
  ☑ Producto incorrecto

Manejo:
  - NO se crea GR
  - Mercancía va a "Almacén Devoluciones"
  - Se genera incidencia con proveedor
  - PO se queda abierta esperando reposición correcta
```

**Para nuestro caso (todo OK), Ana marca "Aceptado" y sigue.**

---

### PASO 8: Confirmación de la GR — Actualización provisional de stock

**Actor:** Ana (confirma) → Sistema (procesa)

```
Ana click en "Confirmar Recepción".

Eventos del sistema:

1. Crear documento GR (Goods Receipt):
   gr_id: GR_2026_0042
   gr_ref: PO_2026_0042
   status: CONFIRMED
   confirmed_by: ana.lopez
   confirmed_at: 2026-07-18 14:23
   warehouse: Madrid Central
   location: Pasillo 3, Estantería B

2. Crear líneas de GR:
   gr_line_id: 1
   product: TORN-M8-30-GAL
   qty_received: 1000
   qty_accepted: 1000
   qty_rejected: 0
   unit_price: 0,15€ (del PO)
   valuation: 150,00€

3. Actualizar stock (PROVISIONAL):
   ANTES:  TORN-M8-30-GAL @ Madrid = 200 uds @ 0,14€/u = 28,00€
   AHORA:  TORN-M8-30-GAL @ Madrid = 1200 uds @ 0,1483€/u = 178,00€
   
   Nuevo cálculo WAC:
     Stock anterior: 200 uds × 0,14€ = 28,00€
     Recepción:     1000 uds × 0,15€ = 150,00€
     Total:         1200 uds @ 178,00€ → WAC = 0,1483€/u

4. Crear Stock Ledger Entry (SLE):
   sle_id: SLE_2026_7891
   product: TORN-M8-30-GAL
   warehouse: Madrid Central
   qty_change: +1000
   valuation_change: +150,00€
   source: GR_2026_0042
   provisional: true  ← flag importante

5. Actualizar estado de PO:
   PO_2026_0042.status: SENT → FULLY_RECEIVED

6. Audit log (inmutable):
   "ana.lopez confirmed GR_2026_0042 for PO_2026_0042 at 2026-07-18 14:23"
```

**¿Por qué "provisional"?** Porque el precio puede cambiar cuando llegue la factura del proveedor.

---

### PASO 9: La factura llega del proveedor

```
(días después)

García envía factura electrónica:
  - Formato: Facturae XML + PDF
  - CIF emisor: B-87654321
  - CIF receptor: B-12345678
  - Número factura: GARCIA-FAC-2026-1523
  - Fecha factura: 2026-07-19
  - Fecha esperada pago: 2026-08-18 (30 días)

┌────────────────────────────────────────────────────────────┐
│ FACTURA GARCIA-FAC-2026-1523                               │
├────────────────────────────────────────────────────────────┤
│ TORN-M8-30-GAL:  1000 uds × 0,148€ = 148,00€             │
│                  (notar: precio cambió de 0,15 a 0,148)   │
│                  García aplicó un descuento comercial     │
│                                                            │
│ Subtotal:          148,00€                                │
│ Descuento pronto pago (2%): -2,96€                        │
│ Base imponible:    145,04€                                │
│ IVA 21%:           30,46€                                 │
│ ─────────────────────────────                              │
│ TOTAL FACTURA:     175,50€                                │
└────────────────────────────────────────────────────────────┘
```

**Cómo entra la factura al sistema:**

| Opción | Pros | Contras |
|--------|------|---------|
| A) Sube manual al CRM | Simple | Doble entrada |
| B) Email + OCR automático | Sin trabajo manual | OCR falla con PDFs mal escaneados |
| C) API del proveedor | Sin error humano | Requiere integración |
| D) SII/VeriFactu pull | Máxima automatización | Depende de AEAT (24-48h delay) |

**Recomendación MVP:** A) + B) en paralelo.

---

### PASO 10: Validación 3-Way Matching automática

**Actor:** Sistema (con Laura supervisando)

```
El sistema ejecuta el 3-way matching:

┌────────────────────────────────────────────────────────────┐
│ 3-WAY MATCH: PO_2026_0042 ↔ GR_2026_0042 ↔ GARCIA-FAC... │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ CHECK 1: Cantidades                                       │
│ ┌────────────────────────────────────────────────┐       │
│ │ Producto    │ PO    │ GR    │ Factura │ Match  │       │
│ ├────────────────────────────────────────────────┤       │
│ │ TORN-M8-30 │ 1000 │ 1000 │ 1000    │ ✅ OK  │       │
│ └────────────────────────────────────────────────┘       │
│                                                            │
│ CHECK 2: Precios unitarios                                │
│ ┌────────────────────────────────────────────────┐       │
│ │ Producto    │ PO    │ GR    │ Factura │ Var%   │       │
│ ├────────────────────────────────────────────────┤       │
│ │ TORN-M8-30 │0,15€ │0,15€  │0,148€   │ -1,33% │       │
│ └────────────────────────────────────────────────┘       │
│                                                            │
│ CHECK 3: Total factura vs PO                              │
│ PO:     181,50€  (150 + 31,50 IVA)                        │
│ Factura: 175,50€ (148 - 2,96 dto + 30,46 IVA)            │
│ Diferencia: 6,00€ (descuento)                             │
│ Variación: -3,30%                                         │
│                                                            │
│ CHECK 4: Proveedor                                         │
│ PO: García B-87654321                                      │
│ Factura: García B-87654321 → ✅ OK                       │
│                                                            │
│ CHECK 5: Almacén                                           │
│ PO: Madrid Central                                         │
│ GR: Madrid Central → ✅ OK                                │
└────────────────────────────────────────────────────────────┘
```

**Tu tolerancia <2% aplicada:**

```
Variación de precio por unidad: 0,15€ → 0,148€ = -1,33%
  → DENTRO de tolerancia (< 2%) → ✅ ACEPTADO AUTOMÁTICO

PERO el descuento comercial hace que la variación
total sea -3,30% → FUERA de tolerancia

El sistema hace matching por línea Y por total:
  Línea por línea: ✅ dentro de tolerancia
  Total factura vs PO: ⚠️ fuera de tolerancia
  → WARNING a Laura (no bloquea)
  → Laura decide si acepta el descuento
  → Queda registrado en audit
```

---

### PASO 11: Cálculo del Price Variance y ajuste de stock

**Actor:** Sistema

```
La factura confirma precio REAL: 0,148€/u
El stock se había valorado provisionalmente a 0,15€/u
Diferencia: -0,002€/u × 1000 uds = -2,00€

Cálculo del price variance:
  Precio PO:           0,150€/u
  Precio Factura:      0,148€/u
  Variance por unidad: -0,002€/u (favorable)
  Cantidad:             1000 uds
  Variance total:      -2,00€ (favorable)

El sistema recalcula el WAC del producto:

ANTES (provisional):
  Stock: 1200 uds
  Valor: 178,00€
  WAC: 0,1483€/u

AHORA (ajustado):
  Stock: 1200 uds
  Valor: 176,00€
  WAC: 0,1467€/u
```

---

### PASO 12: Generación de asientos contables (PGC España)

**Actor:** Sistema → Laura (revisa)

```
Asiento contable generado por la factura GARCIA-FAC-2026-1523:

┌─────────────────────────────────────────────────────────────┐
│ ASIENTO #2026-07-19-0042                                    │
│ Fecha: 2026-07-19                                           │
│ Concepto: Compra tornillería García - PO_2026_0042          │
├─────────────────────────────────────────────────────────────┤
│ DEBE:                                                       │
│   600. Compras de mercaderías           148,00€             │
│   472. H.P. IVA soportado               30,46€             │
│                                                            │
│ HABER:                                                      │
│   400. Proveedores                     175,50€             │
│   609. Rappels por compras               -2,96€            │
└─────────────────────────────────────────────────────────────┘

Asiento secundario (ajuste de stock):
┌─────────────────────────────────────────────────────────────┐
│ DEBE:                                                       │
│   300. Mercaderías (stock)            +148,00€             │
│                                                            │
│ HABER:                                                      │
│   600. Compras                         -150,00€            │
│   798. Diferencias de precio en compras -2,00€             │
└─────────────────────────────────────────────────────────────┘
```

---

### PASO 13: Reportes a la AEAT (SII / VeriFactu / Facturae)

```
⚠️ APLICA SI EL CLIENTE ES EMPRESA ESPAÑOLA CON SII
   (o si vende a Administración Pública)
```

**Estado actual de facturación electrónica en España** (fuente: [Wikipedia · Factura electrónica en España](https://es.wikipedia.org/wiki/Factura_electr%C3%B3nica_en_Espa%C3%B1a)):

```
- Real Decreto 1619/2012: Reglamento general de facturación
- Ley 25/2013: Factura electrónica obligatoria en sector público
- Orden HAP/1074/2014: Punto General de Entrada de Facturas Electrónicas
- SII (2017): Envío de libros IVA en 4 días (opcional para grandes empresas)
- Ley Crea y Crece (2022): Obligatoria para empresas >8M€ facturación
- VeriFactu AEAT: En despliegue progresivo desde 2025
- TicketBAI: Específico del País Vasco foral
```

---

### PASO 14: Stock actualizado y reportes operativos

```
Tu CRM ahora tiene:

Stock actual:
  TORN-M8-30-GAL @ Madrid Central
  Cantidad: 1200 uds
  WAC: 0,1467€/u
  Valor total: 176,00€

KPIs operativos:
  POs activas:                       12
  POs pendientes recibir:            3
  POs parcialmente recibidas:        2
  POs cerradas este mes:             47

  Recepciones pendientes validar:    1
  Facturas pendientes validar:       2
  Discrepancias abiertas:            0

  Valor stock total:                 45.678,32€
  Items en stock:                    1.234
  Almacenes activos:                 3

  Top 5 proveedores por volumen:
    1. García (B-87654321)            38%
    2. Sur Metalúrgica                24%
    3. Distribución Norte             18%
    4. Químicos del Sur               12%
    5. Otros                           8%
```

---

## 🔗 Documentos del walkthrough

Para profundizar en cada paso, ver los markdowns siguientes:
- Estados de la PO → [04 · Estados PO](./04-estados-po.md)
- 3-Way Matching → [03 · Three-Way Matching](./03-three-way-matching.md)
- Estrategias de stock update → [05 · Estrategias stock](./05-estrategias-actualizacion-stock.md)
- Métodos de valoración → [06 · Valoración inventario](./06-metodos-valoracion-inventario.md)
- Formatos de exportación → [07 · Formatos](./07-formatos-exportacion.md)
- Normativa España → [13 · España](./13-normativa-espana.md)

---

*Siguiente: [03 · Three-Way Matching](./03-three-way-matching.md)*
