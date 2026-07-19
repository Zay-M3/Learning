---
session: ordenes-de-compra
title: "Dominios · Órdenes de Compra"
---

# Dominios · Órdenes de Compra

> Documentación de dominio sobre el ciclo **Purchase-to-Pay (P2P)** aplicado a un CRM interno español, previo a cualquier implementación.

**Creado:** Julio 2026
**Contexto:** Investigación de dominio para CRM con módulo de compras
**Mercado objetivo:** España (no Colombia)
**Stack previsto:** Python (Django o FastAPI)
**Idioma:** Español

---

## 📚 Sobre esta documentación

Esta carpeta contiene **15 markdowns** que documentan el dominio completo de gestión de órdenes de compra (Purchase-to-Pay / P2P) desde la perspectiva de un CRM interno que NO integra con el sistema del proveedor.

**Caso de uso:** Una empresa logística española con múltiples almacenes, múltiples proveedores por producto, +1000 POs/mes, tolerancia de discrepancia <2%, reportes contables y operativos, factura electrónica según normativa AEAT.

## 🎯 Lo que NO es esta documentación

- **NO es código**: No hay implementaciones todavía. Es research de dominio.
- **NO es un PRD**: No define features de producto, solo el modelo mental.
- **NO es una traducción**: Es análisis crítico basado en fuentes oficiales y experiencias de industria.

## 🧭 Mapa de lectura recomendado

```
1. 01-introduccion-p2p.md ............... Conceptos básicos y terminología
2. 02-flujo-completo.md ................ Walkthrough paso a paso (EJEMPLO NUMÉRICO)
3. 03-three-way-matching.md ............ El control antifraude de la industria
4. 04-estados-po.md .................... Lifecycle de la Purchase Order
5. 05-estrategias-actualizacion-stock.md Cuándo se actualiza el stock (4 estrategias)
6. 06-metodos-valoracion-inventario.md . FIFO / LIFO / WAC / Standard
7. 07-formatos-exportacion.md .......... PDF / XLSX / CSV / XML / UBL / PEPPOL / Facturae
8. 08-multi-proveedor-variantes-precio.md Mismo producto, distintos proveedores
9. 09-multi-almacen.md ................. Estructura de warehouses y ubicaciones
10. 10-tolerancia-discrepancia.md ...... Tu <2% explicado con edge cases
11. 11-reportes-contables.md ........... PGC España + libros obligatorios
12. 12-reportes-operativos.md .......... KPIs y dashboards
13. 13-normativa-espana.md ............. Ley Crea y Crece / VeriFactu / TicketBAI / SII
14. 14-decisiones-arquitectura-pendientes.md 8 decisiones que hay que tomar
15. 15-bibliografia.md ................. Links oficiales verificados
```

## 🏷️ Tags temáticos

- **Dominio:** Compras, Inventario, Contabilidad
- **Industria:** Distribución, Retail, Logística
- **Mercado:** España (normativa AEAT)
- **Estado:** Research / Pre-implementación

## 📝 Notas de uso

Cada markdown incluye:
- ✅ Definiciones formales (con fuente)
- ✅ Ejemplos numéricos cuando aplica
- ✅ Comparativas entre sistemas del mercado (SAP / Odoo / ERPNext)
- ✅ Decisiones pendientes explícitas
- ⚠️ Anti-patrones documentados

Cuando se arranque la implementación, esta documentación será el **ancla de contexto** para no perder el modelo de dominio.

---

*Última actualización: Julio 2026*