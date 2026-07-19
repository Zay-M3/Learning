---
session: ordenes-de-compra
title: "Normativa España (AEAT, IVA, factura electrónica)"
---

# 13 · Normativa España (AEAT, IVA, factura electrónica)

> **Lo que tu CRM debe conocer específicamente para operar en España.** Ley Crea y Crece, VeriFactu, TicketBAI, SII, Facturae, PGC.

**Creado:** Julio 2026

---

## 🎯 Por qué importa

Aunque tu CRM NO es un software de facturación, debe **conocer y respetar** la normativa española porque:

1. Recibe facturas de proveedores en formatos regulados
2. Genera documentos que pueden acabar en auditorías
3. Algunos clientes exigirán compliance con AA.PP.
4. La normativa cambia频繁 (VeriFactu 2025-2026, Ley Crea y Crece 2022)

> Fuente principal: [Wikipedia · Factura electrónica en España](https://es.wikipedia.org/wiki/Factura_electr%C3%B3nica_en_Espa%C3%B1a)

---

## 📚 Marco normativo español

### Normativa general de facturación

| Norma | Contenido | Vigente desde |
|-------|-----------|---------------|
| **Directiva 2001/115/CE** | Directiva UE sobre facturación | UE |
| **Real Decreto 1619/2012** | Reglamento general de facturación | Dic 2012 |
| **Orden EHA/962/2007** | Facturación telemática | Abr 2007 |
| **Orden PRE/2971/2007** | Facturas electrónicas a AGE | Oct 2007 |

### Normativa de factura electrónica

| Norma | Contenido | Vigente desde |
|-------|-----------|---------------|
| **Ley 25/2013** | Factura electrónica obligatoria en sector público | Dic 2013 |
| **Orden HAP/1074/2014** | Punto General de Entrada de Facturas Electrónicas | Jun 2014 |

### Sistemas de la AEAT (obligatorios progresivamente)

| Sistema | Aplica a | Vigente |
|---------|----------|---------|
| **SII** (Suministro Inmediato de Información) | Empresas grandes + REDEME | Desde jul 2017 (opcional) |
| **Ley Crea y Crece** | Empresas >8M€ facturación | Desde 2022-2024 (progresivo) |
| **VeriFactu** | Todos (progresivamente) | Desde 2025-2026 |

### Normativa foral (País Vasco, Navarra)

| Sistema | Territorio |
|---------|------------|
| **TicketBAI** | Álava, Guipúzcoa, Vizcaya (activa) |
| **BATA** | Navarra |
| **IGIC** (impuesto propio) | Canarias |

---

## 🏛️ SII (Suministro Inmediato de Información)

> Fuente: [Wikipedia · SII](https://es.wikipedia.org/wiki/SII) (no tiene artículo propio, info oficial en AEAT)

### ¿Qué es?

Sistema de la AEAT para que las empresas **envíen sus libros registro de IVA en tiempo real** (4 días desde la operación).

### ¿A quién aplica?

```
Obligatorio para:
  - Empresas con volumen de facturación > 6M€
  - Empresas inscritas en REDEME (Registro de Devolución Mensual del IVA)
  - Grupos de IVA

Voluntario para:
  - Cualquier otra empresa que quiera acogerse
```

### ¿Qué implica para tu CRM?

```
Tu CRM debe poder generar:
  - Libros de IVA soportado (facturas recibidas)
  - Libros de IVA repercutido (facturas emitidas)
  - En formato XML estructurado según AEAT
  - Con timestamps para envío en plazo de 4 días

PERO el envío al SII lo hace el programa contable,
  no tu CRM directamente.
```

---

## 📋 Ley Crea y Crece (Ley 18/2022)

### ¿Qué establece?

```
- Factura electrónica OBLIGATORIA entre empresas
- Para empresas con facturación > 8M€
- Formato Facturae (XML) o equivalente
- Plazo progresivo de entrada en vigor:
  - Empresas > 8M€: obligatorio
  - Empresas < 8M€: voluntario (de momento)
```

### ¿Qué implica para tu CRM?

```
✅ Generar facturas electrónicas en formato Facturae (cuando factures a clientes)
✅ Recibir facturas en formato Facturae de proveedores
✅ Parsear Facturae XML correctamente
✅ Almacenar facturas con su estructura completa
✅ Permitir descarga de facturas para auditoría

⚠️ Tu CRM NO es software de facturación certificado,
   pero debe INTEGRARSE con el que tenga el cliente.
```

---

## 🔍 VeriFactu (sistema AEAT 2025-2026)

> *Nota: VeriFactu no tiene artículo en Wikipedia actualmente. La información proviene de documentación oficial AEAT y comunicación pública del Ministerio de Hacienda.*

### ¿Qué es?

```
VeriFactu es el sistema de la AEAT para verificar la autenticidad
de las facturas emitidas en tiempo real.

Características:
  - Cada factura emitida lleva una "huella digital" (hash)
  - Se envía a la AEAT en el momento de emisión
  - La factura incluye un QR verificable
  - Cualquier persona puede verificar la factura escaneando el QR
  - Es OBLIGATORIO para todos los softwares de facturación
```

### Calendario de despliegue

```
VeriFactu NO se activa de golpe, sino progresivamente:

2025:
  - Fabricantes de software de facturación deben adaptarse
  - Empresas grandes empiezan a usar

2026:
  - Obligatorio para todas las empresas
  - Sanciones para quienes no cumplan
```

### ¿Qué implica para tu CRM?

```
Si tu cliente vende a consumidor final (B2C):
  ⚠️ Tu CRM debería integrarse con un software de facturación
     que SÍ cumpla VeriFactu
  ⚠️ NO generar facturas directamente desde el CRM

Si tu cliente es B2B puro:
  ✅ Tu CRM puede generar "facturas recibidas" sin VeriFactu
  ✅ Tu CRM puede generar "órdenes de compra" sin VeriFactu
  ⚠️ Las FACTURAS EMITIDAS por tu cliente sí deben cumplir
```

---

## 🎫 TicketBAI (País Vasco foral)

### ¿Qué es?

```
TicketBAI es el sistema foral del País Vasco (Álava, Guipúzcoa, Vizcaya)
para la facturación electrónica. Similar a VeriFactu pero con
reglas específicas de cada diputación foral.

Aplica a:
  - Empresas y autónomos en Álava, Guipúzcoa, Vizcaya
  - Facturas emitidas (B2B y B2C)
  - Con diferentes plazos según tamaño de empresa
```

### Específico de TicketBAI

```
- IVA diferente al general (puede ser 0% en algunas operaciones)
- Envío a la diputación foral correspondiente (no AEAT nacional)
- Formato XML propio (TicketBAI)
- Plazo de envío: en el momento o al final del día (configurable)
```

### ¿Qué implica para tu CRM?

```
Si tu cliente opera en País Vasco:
  ⚠️ Generar facturas compatibles con TicketBAI (si es software de facturación)
  ⚠️ Respetar IVA foral
  ⚠️ Envío a la diputación foral correcta

Si tu cliente NO opera en País Vasco:
  ✅ Ignorar TicketBAI
```

---

## 📄 Facturae (formato estándar español)

### ¿Qué es?

> Fuente: [Gobierno de España · Facturae](https://www.facturae.gob.es/)

```
Facturae es el formato XML estándar español para factura electrónica,
definido por el Gobierno de España.

Versiones:
  - Facturae 3.0 (2009)
  - Facturae 3.1 (2012)
  - Facturae 3.2 (2015)
  - Facturae 3.2.1 (2019)
  - Facturae 3.2.2 (última, 2022)
```

### Estructura XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<fe:Facturae xmlns:fe="http://www.facturae.gob.es/formato/Versiones/Facturaev3_2_2.xml">
  <FileHeader>
    <SchemaVersion>3.2.2</SchemaVersion>
    <Modality>I</Modality>
    <InvoiceIssuerType>EM</InvoiceIssuerType>
    <Batch>
      <BatchIdentifier>2026-07-001</BatchIdentifier>
      <InvoicesCount>1</InvoicesCount>
      <TotalInvoicesAmount>
        <TotalAmount>175.50</TotalAmount>
      </TotalInvoicesAmount>
      <TotalOutstandingAmount>
        <TotalAmount>175.50</TotalAmount>
      </TotalOutstandingAmount>
      <TotalExecutableAmount>
        <TotalAmount>175.50</TotalAmount>
      </TotalExecutableAmount>
      <InvoiceCurrencyCode>EUR</InvoiceCurrencyCode>
    </Batch>
  </FileHeader>
  <Parties>
    <SellerParty>
      <TaxIdentification>
        <PersonTypeCode>J</PersonTypeCode>
        <ResidenceTypeCode>R</ResidenceTypeCode>
        <TaxIdentificationNumber>B87654321</TaxIdentificationNumber>
      </TaxIdentification>
      <LegalEntity>
        <CorporateName>Suministros García S.L.</CorporateName>
        <AddressInSpain>
          <Address>Polígono Industrial, Nave 12</Address>
          <PostCode>28021</PostCode>
          <Town>Madrid</Town>
          <Province>Madrid</Province>
          <CountryCode>ESP</CountryCode>
        </AddressInSpain>
      </LegalEntity>
    </SellerParty>
    <BuyerParty>
      <TaxIdentification>
        <PersonTypeCode>J</PersonTypeCode>
        <ResidenceTypeCode>R</ResidenceTypeCode>
        <TaxIdentificationNumber>B12345678</TaxIdentificationNumber>
      </TaxIdentification>
      <LegalEntity>
        <CorporateName>Logística Martín S.L.</CorporateName>
        <AddressInSpain>
          <Address>Calle Logística 123</Address>
          <PostCode>28001</PostCode>
          <Town>Madrid</Town>
          <Province>Madrid</Province>
          <CountryCode>ESP</CountryCode>
        </AddressInSpain>
      </LegalEntity>
    </BuyerParty>
  </Parties>
  <Invoices>
    <Invoice>
      <InvoiceHeader>
        <InvoiceNumber>GARCIA-FAC-2026-1523</InvoiceNumber>
        <InvoiceDocumentType>FC</InvoiceDocumentType>
        <InvoiceClass>OO</InvoiceClass>
      </InvoiceHeader>
      <InvoiceIssueData>
        <IssueDate>2026-07-19</IssueDate>
        <InvoiceCurrencyCode>EUR</InvoiceCurrencyCode>
        <TaxCurrencyCode>EUR</TaxCurrencyCode>
        <LanguageCode>es</LanguageCode>
      </InvoiceIssueData>
      <TaxesOutputs>
        <Tax>
          <TaxTypeCode>01</TaxTypeCode>
          <TaxRate>21.00</TaxRate>
          <TaxableBase>
            <TotalAmount>148.00</TotalAmount>
          </TaxableBase>
          <TaxAmount>
            <TotalAmount>30.46</TotalAmount>
          </TaxAmount>
        </Tax>
      </TaxesOutputs>
      <InvoiceTotals>
        <TotalGrossAmount>148.00</TotalGrossAmount>
        <TotalGrossAmountBeforeTaxes>148.00</TotalGrossAmountBeforeTaxes>
        <TotalTaxOutputs>30.46</TotalTaxOutputs>
        <InvoiceTotal>175.50</InvoiceTotal>
        <TotalOutstandingAmount>175.50</TotalOutstandingAmount>
        <TotalExecutableAmount>175.50</TotalExecutableAmount>
      </InvoiceTotals>
      <Items>
        <InvoiceLine>
          <ItemDescription>Tornillo M8x30 galvanizado (1000 uds)</ItemDescription>
          <Quantity>1000</Quantity>
          <UnitOfMeasure>EA</UnitOfMeasure>
          <UnitPriceWithoutTax>0.148</UnitPriceWithoutTax>
          <TotalCost>148.00</TotalCost>
          <GrossAmount>148.00</GrossAmount>
          <TaxesOutputs>
            <Tax>
              <TaxTypeCode>01</TaxTypeCode>
              <TaxRate>21.00</TaxRate>
              <TaxableBase>
                <TotalAmount>148.00</TotalAmount>
              </TaxableBase>
              <TaxAmount>
                <TotalAmount>30.46</TotalAmount>
              </TaxAmount>
            </Tax>
          </TaxesOutputs>
        </InvoiceLine>
      </Items>
    </Invoice>
  </Invoices>
</fe:Facturae>
```

### ¿Cómo lo usa tu CRM?

```
✅ Recibir facturas Facturae de proveedores
✅ Parsear el XML para extraer datos contables
✅ Validar que el XML cumple schema XSD
✅ Almacenar el archivo para auditoría

✅ (Si tu cliente vende a AA.PP.) Generar Facturae
```

---

## 💰 Tipos de IVA en España

```
General:        21%  (la mayoría de productos)
Reducido:       10%  (alimentación, libros, transporte, hostelería)
Superreducido:   4%  (pan, leche, libros básicos, vivienda VPO, medicamentos)
Exento:          0%  (Canarias IGIC, Ceuta y Melilla IPSI, operaciones exentas)
```

### Reglas especiales

```
Inversión del sujeto pasivo (ISP):
  - Proveedor extracomunitario (fuera de UE)
  - El comprador autoliquida IVA
  - IVA va en cuenta 472 con flag ISP

Recargo de equivalencia (RE):
  - Autónomos en régimen de recargo
  - Recargo adicional sobre IVA (5,2%, 1,4%, 0,5%)
  - IVA total = IVA + RE

Retención IRPF:
  - Profesionales (no empresas)
  - 15% general, 7% nuevos profesionales
  - El cliente retiene, no paga al proveedor
  - Cuenta 4751 H.P. Acreedor por retenciones
```

---

## 📅 Conservación de documentos

```
Facturas:           4 años mínimo (5 años para libros IVA)
Libros contables:   5 años
Documentos P2P:     4 años mínimo
Audit logs:         10 años (compliance internacional)
```

**⚠️ Importante:** en formato electrónico, no solo en papel. Deben ser consultables.

---

## ✅ Checklist normativa España para tu CRM

```
┌──────────────────────────────────────────────────────────────┐
│ CHECKLIST NORMATIVA ESPAÑA PARA TU CRM                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ DATOS FISCALES:                                              │
│   ✅ CIF/NIF del proveedor validado (formato España)         │
│   ✅ CIF/NIF propio (B-12345678 formato jurídico SL)         │
│   ✅ IBAN para pagos (ES91 2100 0418 4502 0005 1332)        │
│                                                              │
│ IVA:                                                         │
│   ✅ Tipos: 21% general, 10% reducido, 4% superreducido     │
│   ✅ IVA 0% para Canarias, Ceuta, Melilla (exento)          │
│   ✅ Inversión del sujeto pasivo (proveedor extracomunitario│
│   ✅ Recargo de equivalencia (autónomos)                     │
│                                                              │
│ IRPF:                                                        │
│   ✅ Retención 15% profesionales (alquileres, servicios)     │
│   ✅ Retención 7% nuevos profesionales (< 2 años)           │
│                                                              │
│ FACTURACIÓN ELECTRÓNICA:                                     │
│   ⚠️ Ley Crea y Crece (2022): obligatoria >8M€ facturación │
│   ⚠️ VeriFactu AEAT: en despliegue progresivo              │
│   ⚠️ TicketBAI: País Vasco / Navarra forales               │
│   ✅ Facturae: si vende a AA.PP.                            │
│                                                              │
│ FORMATO DE NÚMERO DE FACTURA:                                │
│   ✅ Formato: FAC-AAAA-NNNNNN (España)                       │
│   ✅ Sin saltos en la numeración                             │
│   ✅ Series separadas por tipo (factura, rectificativa)     │
│                                                              │
│ PLAZOS:                                                      │
│   ✅ Conservar facturas: 4 años mínimo (5 para libros IVA)  │
│   ✅ Plazo pago a proveedor: 30 días por defecto            │
│   ✅ Ley 15/2010: tope 60 días (sanciones si excede)        │
│                                                              │
│ IDIOMA:                                                      │
│   ✅ Español obligatorio en facturas a AA.PP.               │
│   ✅ Idiomas co-oficiales permitidos en facturas privadas   │
│      (catalán, euskera, gallego, valenciano)                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📚 Referencias

- Wikipedia: [Factura electrónica en España](https://es.wikipedia.org/wiki/Factura_electr%C3%B3nica_en_Espa%C3%B1a)
- AEAT: [Suministro Inmediato de Información](https://www.agenciatributaria.es/)
- Gobierno de España: [Facturae](https://www.facturae.gob.es/)
- Wikipedia: [PEPPOL](https://en.wikipedia.org/wiki/PEPPOL)

---

*Siguiente: [14 · Decisiones de arquitectura pendientes](./14-decisiones-arquitectura-pendientes.md)*
