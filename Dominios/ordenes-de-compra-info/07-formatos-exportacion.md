# 07 · Formatos de exportación de Purchase Order

> **PDF, XLSX, CSV, XML, UBL, PEPPOL, Facturae.** Cuál soporta qué proveedor, cuándo usar cada uno.

**Creado:** Julio 2026

---

## 🎯 Por qué importa

Tu requisito confirmado: **el proveedor recibe la PO en el formato que quiera**. Tu CRM debe poder exportar en múltiples formatos porque NO hay un estándar único que todos los proveedores acepten.

> *"Electronic data interchange (EDI) is the concept of businesses electronically communicating information that was traditionally communicated on paper, such as purchase orders, advance ship notices, and invoices."*
> — Fuente: [Wikipedia · Electronic data interchange](https://en.wikipedia.org/wiki/Electronic_data_interchange)

---

## 📊 Pirámide de formatos (de menos a más técnico)

```
                    PDF  ← 100% proveedores, pero NO procesable
                    ───
                    XLSX ← 60% proveedores, semi-procesable
                    ───
                    CSV  ← 40% proveedores, técnico simple
                    ───
                    XML  ← 20% proveedores, EDI básico
                    ───
                    UBL  ← 5% proveedores grandes, estándar internacional
                    ───
                    PEPPOL ← 2% (pero crece rápido, B2G obligatorio en UE)
```

---

## 📋 Formatos en detalle

### 1. PDF (Portable Document Format)

```
Uso:        100% de proveedores en España
Procesable: ❌ No (requiere OCR para extraer datos)
Firma:      ✅ Soporta firma digital
Envío:      Email, WhatsApp, impreso

Plantilla recomendada:
  - Logo empresa arriba
  - Cuadro con datos fiscales (CIF, dirección, IBAN)
  - Numeración visible: PO_2026_0042
  - Tabla con líneas (SKU, descripción, cant, precio, total)
  - Subtotal + desglose IVA + total
  - Términos de pago
  - Fecha emisión + fecha esperada entrega
  - Datos de contacto

Librería Python: reportlab, WeasyPrint, FPDF
```

### 2. XLSX (Excel)

```
Uso:        60% de proveedores en España
Procesable: ✅ Parcialmente (pueden editar o hacer upload a su sistema)
Firma:      ❌ No estándar (pueden usar macros)
Envío:      Email, OneDrive, Google Drive

Ventajas:
  - Proveedor puede agregar info adicional (su ref, su precio)
  - Permite usar fórmulas propias
  - Familiar para cualquier administrativo

Librería Python: openpyxl, xlsxwriter
```

### 3. CSV (Comma Separated Values)

```
Uso:        40% de proveedores en España
Procesable: ✅ Totalmente (cualquier sistema puede parsearlo)
Firma:      ❌ No estándar
Envío:      Email, FTP, SFTP

Estructura típica:
  sku,descripcion,cantidad,precio_unitario,total
  TORN-M8-30-GAL,Tornillo M8x30 galvanizado,1000,0.15,150.00
  ARAN-M8-30-GAL,Arandela M8 galvanizada,2000,0.02,40.00

Librería Python: csv (stdlib)
```

### 4. XML (Extensible Markup Language)

```
Uso:        20% de proveedores en España
Procesable: ✅ Totalmente (schema-validable)
Firma:      ✅ Soporta XAdES, XMLDSig
Envío:      Email, SFTP, AS2

Variantes:
  - XML custom (tu propio schema)
  - EDIFACT (pipe-delimited, UN/CEFACT)
  - ANSI X12 (USA, segment-based)
  - UBL (Universal Business Language, ISO/IEC 19845)

Librería Python: lxml, xml.etree.ElementTree
```

### 5. UBL (Universal Business Language)

> Fuente: [Wikipedia · Universal Business Language](https://en.wikipedia.org/wiki/Universal_Business_Language)

```
Uso:        5% (proveedores grandes + sector público internacional)
Procesable: ✅ Totalmente
Estándar:   ISO/IEC 19845, OASIS
Schema:     UBL 2.1 (versión actual)

Documentos UBL relevantes para P2P:
  - Order (PO)
  - OrderResponseSimple (PO Acknowledgement)
  - DespatchAdvice (ASN - Advance Ship Notice)
  - ReceiptAdvice (GR)
  - Invoice
  - CreditNote

Ejemplo abreviado:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Order xmlns="urn:oasis:names:specification:ubl:schema:xsd:Order-2">
  <ID>PO_2026_0042</ID>
  <IssueDate>2026-07-15</IssueDate>
  <BuyerCustomerParty>
    <Party>
      <PartyIdentification>
        <ID>B-12345678</ID>
      </PartyIdentification>
    </Party>
  </BuyerCustomerParty>
  <SellerSupplierParty>
    <Party>
      <PartyIdentification>
        <ID>B-87654321</ID>
      </PartyIdentification>
    </Party>
  </SellerSupplierParty>
  <OrderLine>
    <LineItem>
      <ID>1</ID>
      <Quantity unitCode="EA">1000</Quantity>
      <Price>
        <PriceAmount currencyID="EUR">0.15</PriceAmount>
      </Price>
      <Item>
        <Name>Tornillo M8x30 galvanizado</Name>
        <SellersItemIdentification>
          <ID>TORN-M8-30-GAL</ID>
        </SellersItemIdentification>
      </Item>
    </LineItem>
  </OrderLine>
</Order>
```

Librería Python: python-ubl, generación custom con jinja2
```

### 6. Facturae (estándar español de e-factura)

```
Uso:        Obligatorio para facturas a AA.PP. (Ley 25/2013)
Procesable: ✅ Totalmente
Estándar:   Gobierno de España
Schema:     Versión 3.2.x (última)
Web oficial: https://www.facturae.gob.es/

⚠️ Aunque "Facturae" es para facturas, su esquema XML 
   también puede adaptarse para órdenes de compra si el
   proveedor lo acepta.

Librería Python: facturae-python, generación custom
```

### 7. PEPPOL (red de e-procurement)

> Fuente: [Wikipedia · PEPPOL](https://en.wikipedia.org/wiki/PEPPOL)

```
Uso:        2.5M+ organizaciones en 111 países (feb 2026)
Procesable: ✅ Totalmente
Estándar:   OpenPeppol (Bélgica)
Formato:    UBL sobre red PEPPOL

Arquitectura:
  - SML (Service Metadata Locator): base de datos central
  - SMP (Service Metadata Publisher): BD por participante
  - AP (Access Point): API de entrega

Adopción en España:
  - Creciendo rápido en sector público
  - Obligatorio en algunos concursos públicos europeos
  - A implementar solo si tu cliente quiere vender a AA.PP.

Librería Python: ramps-client (PEPPOL Access Point)
```

---

## 🎯 Roadmap de formatos para tu CRM

### MVP (Fase 1)

```
✅ PDF (obligatorio)
✅ XLSX (obligatorio)
✅ CSV (obligatorio)
✅ XML custom (recomendable)
```

### Fase 2 (cuando crezcas)

```
📋 UBL 2.1 (cuando tengas clientes europeos grandes)
📋 Facturae (si vendes a AA.PP.)
```

### Fase 3 (cuando tengas clientes enterprise)

```
📋 PEPPOL (si vendes a multinacionales o B2G)
📋 EDIFACT / ANSI X12 (si tienes proveedores con sistemas legacy)
```

---

## 🏗️ Implementación recomendada

### Patrón Strategy

```
Formatos de Exportación
├── PDFExporter      → ReportLab / WeasyPrint
├── XLSXExporter     → openpyxl
├── CSVExporter      → csv stdlib
├── XMLExporter      → jinja2 + lxml
├── UBLExporter      → jinja2 + lxml (UBL schema)
├── FacturaeExporter → jinja2 + lxml (Facturae schema)
└── PeppolExporter   → API client (ramps)
```

Cada exporter implementa la misma interfaz:

```
interface POExporter:
    function export(po: PurchaseOrder, options: dict) -> ExportedFile
```

Donde `ExportedFile` es:

```
ExportedFile:
    - filename: str
    - content: bytes
    - mime_type: str
    - extension: str
```

### Selección de formato por proveedor

```
Tabla: supplier_format_preference
  - supplier_id
  - format (PDF, XLSX, CSV, XML, UBL, Facturae)
  - priority (1-5, en orden de preferencia)
  - active (bool)
```

Cuando se envía una PO:
1. Sistema consulta preferencias del proveedor
2. Genera en el formato de mayor prioridad
3. Si falla, fallback al siguiente
4. Si todos fallan, alert al operador

---

## 📊 Decisión por tamaño de proveedor

| Tamaño proveedor | Formato típico | Razón |
|------------------|----------------|-------|
| Autónomo / Micro | PDF | Sin sistema, recibe email |
| Pyme (< 10 empleados) | XLSX o PDF | Sin EDI, usa Excel |
| Pyme mediana | XLSX + CSV | Algún proceso batch |
| Empresa grande | UBL o XML propio | Tiene ERP que integra |
| Multinacional | UBL / PEPPOL | Compliance corporativo |
| Sector público | Facturae | Obligatorio por ley |

---

## 📚 Referencias

- Wikipedia: [Electronic data interchange](https://en.wikipedia.org/wiki/Electronic_data_interchange)
- Wikipedia: [Universal Business Language](https://en.wikipedia.org/wiki/Universal_Business_Language)
- Wikipedia: [PEPPOL](https://en.wikipedia.org/wiki/PEPPOL)
- Wikipedia: [Invoice](https://en.wikipedia.org/wiki/Invoice) (Electronic subsection)
- Gobierno de España: [Facturae](https://www.facturae.gob.es/)

---

*Siguiente: [08 · Multi-proveedor con variantes de precio](./08-multi-proveedor-variantes-precio.md)*
