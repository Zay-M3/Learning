# 10 · Tolerancia de discrepancia <2%

> **Cómo se calcula, dónde se aplica, qué pasa con los edge cases.**

**Creado:** Julio 2026

---

## 🎯 Tu requisito

Confirmado: **tolerancia de discrepancia <2%**.

Esto significa que tu sistema es **MÁS estricto** que la industria (típico 5%).

---

## 📐 Definición formal

La tolerancia se aplica a **3 niveles**:

### Nivel 1: Variación por unidad (price line variance)

```
variacion = |precio_factura - precio_PO| / precio_PO × 100

Si variacion >= 2% → WARNING al aprobador
Si variacion < 2% → OK automático
```

### Nivel 2: Variación por total de línea (incluye descuentos)

```
variacion = |total_linea_factura - total_linea_PO| / total_linea_PO × 100

Si variacion >= 2% → WARNING
Si variacion < 2% → OK
```

### Nivel 3: Variación por total de factura

```
variacion = |total_factura - total_PO| / total_PO × 100

Si variacion >= 2% → WARNING
Si variacion < 2% → OK
```

---

## 🎚️ Tolerancia compuesta (recomendación)

```
Regla primaria: variacion < 2%
Regla secundaria: variacion_absoluta < 5€
(lo que sea más estricto gana)

Justificación:
  - 2% es estricto vs industria (típico 5%)
  - 5€ absoluto cubre el caso de PO pequeñas
  - Evita que PO de 1€ se bloquee por 0,02€ de diferencia
```

### Ejemplo comparativo

```
PO de 10€ (muy pequeña):
  - Tolerancia 2%: hasta 0,20€
  - Tolerancia absoluta 5€: hasta 5€
  - Aplica la primaria: hasta 0,20€
  
  Si factura es 10,10€ (variación 1%):
    - 1% < 2% → OK automático
    - 0,10€ < 5€ → OK automático
    - ✅ ACEPTADO

PO de 1000€ (grande):
  - Tolerancia 2%: hasta 20€
  - Tolerancia absoluta 5€: hasta 5€
  - Aplica la secundaria: hasta 5€
  
  Si factura es 1003€ (variación 0,3%):
    - 0,3% < 2% → OK
    - 3€ < 5€ → OK
    - ✅ ACEPTADO
    
  Si factura es 1010€ (variación 1%):
    - 1% < 2% → OK
    - 10€ > 5€ → ❌ WARNING manual
    - ⚠️ REQUIERE APROBACIÓN
```

---

## 🚨 Edge cases (decisiones pendientes)

### Edge Case A: Diferencia EXACTA de 1.99%

```
¿Aceptar o rechazar?

Recomendación: ✅ ACEPTAR (es <2%)
Implementación: usar comparación estricta (< 2.0)
```

### Edge Case B: Diferencia de 2.01%

```
¿Aceptar con WARNING o rechazar?

Recomendación: ⚠️ WARNING manual (no rechazo)
Implementación: comparación estricta → escala a usuario
```

### Edge Case C: Diferencia 50% pero justificada

```
Ejemplo: descuento por volumen pactado en contrato marco
  PO: 1000 unidades a 0,15€/u = 150€
  Factura: 1000 unidades a 0,075€/u = 75€ (-50% por descuento)

Recomendación: 🔓 OVERRIDE con motivo obligatorio
Implementación:
  - Carlos selecciona "Override por contrato"
  - Sistema pide: motivo (texto), referencia del contrato
  - Audit log con hash inmutable
  - Aprueba nivel 2+
```

### Edge Case D: Diferencia 200%

```
Ejemplo: precio factura 10× el del PO
  PO: 0,15€/u
  Factura: 1,50€/u

Recomendación: 🚫 ESCALAR a dirección
Implementación:
  - Bloqueo automático (no se puede override con nivel 2)
  - Escala a dirección
  - Posible cancelación de PO + acción legal
```

### Edge Case E: Línea con 100% descuento (muestra gratis)

```
PO: 100 unidades a 0,15€/u
Factura: 100 unidades a 0€/u (muestra gratis)

Recomendación: ⚠️ APROBAR con flag de auditoría
Implementación:
  - WARNING (no rechazo)
  - Marca como "muestra" en la línea
  - Audit log específico
  - Cuenta contable 778 (ingresos extraordinarios)
```

### Edge Case F: Línea con precio 0 (regalo)

```
Igual que E. WARNING + flag de auditoría.
```

### Edge Case G: Diferencia <2% pero 0,50€ absoluto en PO pequeña

```
PO: 1€ total
Factura: 1,50€ (variación 50%)

Recomendación: 🚫 BLOQUEAR (combinar % + mínimo)
Implementación: aplicar regla compuesta
  - 50% > 2% → WARNING
  - 0,50€ < 5€ → OK por absoluto
  
  → Decisión: la regla primaria (% < 2%) es más restrictiva → BLOQUEAR
```

---

## 🔐 Override y auditoría

### Override permitido por nivel

| Nivel | Puede override | Requiere motivo |
|-------|----------------|-----------------|
| 1 (Comprador) | ❌ No | — |
| 2 (Manager) | ✅ Hasta 10% | ✅ Texto obligatorio |
| 3 (Director) | ✅ Hasta 50% | ✅ Texto + referencia contrato |
| 4 (DG) | ✅ Cualquiera | ✅ Texto + aprobación dual |

### Audit log de override

```
Cada override queda registrado con:
  - usuario_id
  - timestamp
  - documento original (PO, GR, Invoice)
  - monto original vs real
  - variacion_pct
  - motivo (texto libre)
  - nivel_aprobador
  - hash_inmutable (SHA-256 del registro completo)
```

### Implementación con hash inmutable

```
function log_override(override_data):
    override_data.timestamp = now()
    override_data.hash = sha256(json.dumps(override_data, sort_keys=True))
    save_to_audit_table(override_data)

# Nadie puede modificar el registro sin invalidar el hash
# Esto cumple con requisitos de auditoría forense
```

---

## 📊 Aplicación en diferentes contextos

### Over-receipt (cantidad)

```
Regla específica para cantidad:

┌──────────────────────────────────────────────────────────┐
│ REGLAS PARA OVER-RECEIPT (tolerancia <2% que pediste)  │
├──────────────────────────────────────────────────────────┤
│ Diferencia <2%: aceptar automáticamente con flag        │
│ Diferencia 2-10%: requiere aprobación del manager      │
│ Diferencia >10%: BLOQUEO total, escalado a dirección  │
│                                                          │
│ ⚠️ OVER-RECEIPT ES RIESGO DE FRAUDE                    │
│    (el proveedor puede estar inflando facturas)         │
└──────────────────────────────────────────────────────────┘
```

### Short-receipt (cantidad)

```
Regla específica para short-receipt:

Diferencia <2%: aceptar automáticamente (recepción parcial)
Diferencia >=2%: WARNING al aprobador
  - Opción A: Aceptar parcial + PO con pendiente
  - Opción B: Rechazar todo (devolución)
  - Opción C: Short-close (cerrar línea)
```

### Producto dañado

```
Si hay unidades dañadas:
  - Separar unidades aceptadas de dañadas
  - Dañadas van a QUARANTINE
  - Stock NO se actualiza con dañadas
  - Generar RMA (Return Merchandise Authorization)
  - Notificación automática al proveedor
```

### Producto equivocado

```
Si producto recibido ≠ producto esperado:
  - NO crear GR
  - Toda la línea va a RETURN zone
  - Notificación al proveedor
  - PO se queda abierta esperando reposición
```

---

## 🎯 Recomendación final para tu CRM

### Configuración por defecto

```yaml
tolerance_config:
  price_variance_pct: 2.0          # Por unidad
  line_variance_pct: 2.0           # Por línea total
  invoice_variance_pct: 2.0        # Por factura total
  absolute_variance_eur: 5.0       # Mínimo absoluto
  qty_over_receive_pct: 2.0        # Over-receipt
  qty_short_receive_pct: 2.0       # Short-receipt
  
override_levels:
  level_2_max_pct: 10.0            # Manager puede aceptar hasta 10%
  level_3_max_pct: 50.0            # Director puede aceptar hasta 50%
  level_4_max_pct: 100.0           # DG puede aceptar cualquier cosa
  
audit:
  hash_algorithm: SHA-256
  retention_years: 10              # 10 años para compliance español
```

### UI: cómo se muestra

```
┌──────────────────────────────────────────────────────────┐
│ VALIDACIÓN 3-WAY MATCH: PO_2026_0042                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ Resultado: ⚠️ WARNING (no bloqueante)                   │
│                                                          │
│ Detalle:                                                │
│   Variación por línea: 1,33% (< 2% ✅)                 │
│   Variación total:    3,30% (> 2% ⚠️)                  │
│   Variación absoluta: 6,00€ (> 5€ ⚠️)                  │
│                                                          │
│ Causa probable: descuento comercial no esperado         │
│                                                          │
│ Acciones:                                               │
│   [✅ Aceptar con override]  ← requiere motivo          │
│   [❌ Rechazar factura]                                  │
│   [📞 Contactar proveedor]                              │
│   [📝 Solicitar factura corregida]                      │
└──────────────────────────────────────────────────────────┘
```

---

## 📚 Referencias

- Wikipedia: [Purchase-to-pay](https://en.wikipedia.org/wiki/Purchase-to-pay)
- Wikipedia: [Inventory valuation](https://en.wikipedia.org/wiki/Inventory_valuation)

---

*Siguiente: [11 · Reportes contables](./11-reportes-contables.md)*
