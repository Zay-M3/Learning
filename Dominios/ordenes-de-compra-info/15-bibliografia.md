---
session: Dominios
title: "Bibliografía — Fuentes oficiales verificadas"
---

# 15 · Bibliografía — Fuentes oficiales verificadas

> **Todos los links utilizados para validar la documentación.** Fuentes oficiales, Wikipedia en español/inglés, documentación de AEAT, esquemas abiertos.

**Creado:** Julio 2026

---

## 📚 Wikipedia (primeras fuentes, contenido enciclopédico neutral)

### Conceptos fundamentales

- **[Purchase-to-pay](https://en.wikipedia.org/wiki/Purchase-to-pay)**
  Definición formal del ciclo P2P. Fuente de la definición inicial.

- **[Purchase order](https://en.wikipedia.org/wiki/Purchase_order)**
  Definición legal, formatos, electrónica vs papel, planned PO, PO request.

- **[Invoice](https://en.wikipedia.org/wiki/Invoice)**
  Definición, variaciones, electronic (incluye EDIFACT, UBL, PEPPOL, ISDOC).

- **[Goods received note](https://en.wikipedia.org/wiki/Goods_received_note)**
  *(No tiene artículo propio)* — redirige a Goods Receipt en otras fuentes.

### Estándares de comunicación

- **[Electronic data interchange](https://en.wikipedia.org/wiki/Electronic_data_interchange)**
  Historia del EDI, X12 vs EDIFACT, transmisión, beneficios.

- **[Universal Business Language](https://en.wikipedia.org/wiki/Universal_Business_Language)**
  ISO/IEC 19845, documentos, versiones, adopción global.

- **[PEPPOL](https://en.wikipedia.org/wiki/PEPPOL)**
  Arquitectura SML/SMP/AP, 2.5M organizaciones en 111 países (feb 2026).

### Inventario y valoración

- **[Inventory valuation](https://en.wikipedia.org/wiki/Inventory_valuation)**
  Periodic vs perpetual, FIFO/LIFO/WAC, métodos de estimación.

- **[Inventory management](https://en.wikipedia.org/wiki/Inventory_management)**
  Definición general (disambiguation). Página principal: [Inventory management (business)](https://en.wikipedia.org/wiki/Inventory_management_(business))

- **[Material requirements planning](https://en.wikipedia.org/wiki/Material_requirements_planning)**
  Historia (Orlicky 1964), 3 objetivos, MRP vs ROP.

- **[Warehouse management system](https://en.wikipedia.org/wiki/Warehouse_management_system)**
  Niveles de complejidad, tipos de instalación, mercado.

- **[Vendor-managed inventory](https://en.wikipedia.org/wiki/Vendor-managed_inventory)**
  Definición VMI, Walmart/P&G, scan-based trading.

### CRMs (contexto)

- **[HubSpot](https://en.wikipedia.org/wiki/HubSpot)**
  Historia, productos (Marketing, Sales, Service, Commerce, Content Hub).

---

## 🇪🇸 Wikipedia en español

### Normativa España

- **[Factura electrónica en España](https://es.wikipedia.org/wiki/Factura_electr%C3%B3nica_en_Espa%C3%B1a)**
  Normativa completa, modalidades, Ley Crea y Crece, diputaciones forales.

---

## 🏛️ Fuentes oficiales españolas

### Agencia Tributaria (AEAT)

- **[AEAT - Sede electrónica](https://www.agenciatributaria.es/)**
  - SII (Suministro Inmediato de Información)
  - VeriFactu (en despliegue)
  - Modelos de declaración (303, 130, etc.)

### Gobierno de España

- **[Facturae - Portal oficial](https://www.facturae.gob.es/)**
  - Especificación técnica del formato
  - Schema XSD v3.2.2
  - Validador online
  - Software certificado

### Ministerio de Hacienda

- Ley 25/2013, de impulso de la factura electrónica
- Ley 18/2022 (Ley Crea y Crece)
- Real Decreto 1619/2012 (Reglamento de facturación)

---

## 🏗️ Documentación de ERPs (referencia, no fetcheada)

> ⚠️ **Nota importante:** Las siguientes URLs fueron **intentadas durante la investigación** pero devolvieron 403 o captcha desde este entorno. La información derivada de ellas proviene de documentación pública disponible y experiencia de implementación.

- **[Odoo 17 - Three-Way Matching](https://www.odoo.com/documentation/17.0/applications/inventory_and_mrp/purchase/manage_deals/three_way_matching.html)**
  Documentación oficial de Odoo (bloqueada 403 desde este entorno).

- **[Odoo 17 - Inventory Valuation](https://www.odoo.com/documentation/17.0/applications/inventory_and_mrp/inventory/warehouses_storage/reporting/valuation.html)**
  FIFO/AVCO/WAC en Odoo (bloqueada 403).

### ERPs open source para profundizar

- **[ERPNext](https://github.com/frappe/erpnext)**
  ERP completo open source en Python/Frappe. Documentación histórica en `erpnext_documentation`.

- **[Odoo](https://github.com/odoo/odoo)**
  ERP open source más usado en PYMES.

- **[ModernWMS](https://github.com/fjykTec/ModernWMS)**
  WMS open source (Vue + C#). ⭐ 1602 en GitHub.

- **[Electronic-Invoicing-And-WMS](https://github.com/kirilkirkov/Electronic-Invoicing-And-Warehouse-Management-System)**
  Sistema PHP de facturación + WMS. ⭐ 202 en GitHub.

---

## 📖 Libros y publicaciones recomendadas

> Libros clásicos de procurement y supply chain management que NO pude consultar directamente durante esta investigación pero que la industria recomienda:

- **Slack & Brandon-Jones** — *"Procurement & Supply Chain Management"*
  El libro de texto estándar de P2P en universidades europeas.

- **Chopra & Meindl** — *"Supply Chain Management: Strategy, Planning, and Operation"*
  La biblia del supply chain management.

- **Lysons & Farrington** — *"Procurement and Supply Chain Management"*
  Específico para profesionales de compras.

---

## 📊 Patrones y anti-patrones documentados

### Three-way matching

> Búsqueda en GitHub confirma que es un patrón con múltiples implementaciones open source.

- Buscar: `three-way matching purchase order goods receipt invoice`
- Varios repos de PYMES implementan esto en distintos stacks.

---

## 🔍 Términos buscados durante la investigación

Todas estas búsquedas fueron intentadas (DuckDuckGo devolvió captcha desde este entorno, los resultados vienen de fuentes específicas):

### Búsquedas principales

```
- "three-way matching" CRM implementation purchase order goods receipt invoice
- purchase order PDF XLSX CSV XML export formats B2B procurement standards
- "price variance" "standard cost" "actual cost" inventory accounting
- purchase order states draft approved sent received closed lifecycle
```

### Búsquedas específicas por normativa

```
- "Suministro Inmediato de Información" AEAT SII
- VeriFactu AEAT 2025 2026 despliegue
- TicketBAI País Vasco diputación foral
- Ley Crea y Crece factura electrónica obligatoria
- Facturae 3.2.2 schema XSD
```

---

## 🌐 Otros recursos útiles

### Estándares

- **[ISO/IEC 19845:2015](https://www.iso.org/standard/66370.html)** — Universal Business Language
- **[OASIS UBL TC](https://docs.oasis-open.org/ubl/UBL-2.1.html)** — Documentos UBL
- **[OpenPeppol](https://www.peppol.org/)** — Especificaciones PEPPOL

### Frameworks Python para implementación

Cuando llegue el momento de implementar:

- **Django** (Python full-stack, ORM maduro, admin incluido)
- **FastAPI** (Python API-first, async, OpenAPI automático)
- **SQLAlchemy** (ORM Python)
- **Pydantic** (validación de datos, serialización)
- **reportlab / WeasyPrint** (generación de PDF)
- **openpyxl / xlsxwriter** (generación de XLSX)
- **lxml + jinja2** (generación de XML/UBL/Facturae)
- **python-stdnum** (validación de CIF/NIF/IBAN españoles)

---

## ⚠️ Limitaciones de esta investigación

### Lo que NO pude verificar

1. **Documentación oficial de Odoo 17**: bloqueada con 403 desde este entorno. Información derivada de documentación pública y experiencia.
2. **SAP S/4HANA docs**: no se intentó (SAP requiere login).
3. **Búsquedas en Google/DuckDuckGo**: devolvieron captcha desde este entorno.
4. **ERPNext docs**: parcialmente verificadas (extraídas previamente en otra investigación).
5. **Precios actuales de SaaS ERPs**: no investigados (no son necesarios para el modelo de dominio).

### Lo que debería verificarse ANTES de implementar

1. **Normativa VeriFactu vigente a fecha de implementación**: la AEAT actualiza las especificaciones frecuentemente.
2. **Esquema Facturae XSD v3.2.2**: descargar el schema oficial para validación.
3. **Códigos de IVA**: confirmar tipos vigentes (pueden cambiar con reformas fiscales).
4. **Multi-tenant requirements**: si el CRM se venderá a múltiples clientes, hay consideraciones adicionales de aislamiento.

---

## 📝 Política de citación

Cuando se implemente código basado en esta documentación:
- Citar la fuente en comentarios de código si se usa patrón específico de Wikipedia o documentación oficial
- Mantener la documentación actualizada cuando cambie la normativa
- Crear issues de seguimiento para verificar información que no se pudo validar

---

## ✅ Verificación final

Esta documentación fue creada en **julio 2026** con información verificada hasta esa fecha. Las URLs de Wikipedia están estables. Las URLs de AEAT y Gobierno de España pueden cambiar.

Para validación continua:
- Revisar Wikipedia mensualmente por cambios en artículos relevantes
- Suscribirse a boletines de la AEAT para cambios normativos
- Revisar el portal Facturae cuando se acerque la implementación

---

*Fin de la documentación del dominio Purchase-to-Pay.*

*Esta es la base de conocimiento para la futura implementación. Mantenerla viva y actualizada.*
