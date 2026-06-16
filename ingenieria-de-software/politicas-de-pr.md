# Políticas de Pull Requests

> Un PR no es un commit, es una unidad de revisión. Si el reviewer no puede leerlo entero y entenderlo, no sirve — y eso pasa por encima de las 400 líneas.

---

## Tamaño de PRs

### Por qué importa

El tamaño del PR impacta directamente la calidad de la revisión. La intuición de que "un PR grande es más eficiente porque mergeás todo de una" está contradicha por los datos.

### Qué dicen los estudios

**Microsoft Research** (McIntosh et al., 2016) — análisis de millones de PRs en proyectos open source (Qt, OpenStack, Android):

- PRs de **200-400 LOC** son el sweet spot: defect density más baja, review más rápida
- PRs de **1000-2000 LOC** tienen defect density **2-3× más alta** que los pequeños
- PRs de **>2000 LOC** casi no se revisan bien: los reviewers aprueban sin leer

**Google** (Sadowski et al., ICSE 2018) — datos internos:

- Promedio de PRs: ~50 LOC
- Límite blando interno: **300 LOC** para reviews normales
- Límite duro para reviewers: ~1000 LOC, después de eso no se revisa bien
- Google usa herramientas internas para forzar la división cuando un PR es muy grande

**Resumen:** el sweet spot está entre **200 y 400 LOC**. Superar las 1000 debería ser excepción documentada.

### Política de tamaño recomendada

```
Límite por PR:
- 500 LOC de producción
- 1500 LOC de tests
- 2000 LOC total
```

Si se pasa de cualquiera, dividir.

### Política de ratio test/prod

```
Bug fix:     0.5×  (medio test por cada línea de prod)
Feature:     1.0×  (al menos un test por cada línea de prod)
Refactor:    0.3×  (refactor no debería cambiar comportamiento)
```

Si un PR de feature tiene 500 LOC de prod y solo 100 LOC de tests, no está listo aunque pase el límite de tamaño.

---

## Stacked PRs (PRs apilados)

### El problema

Una feature nueva grande (2000-5000 LOC) no cabe en un PR sano. ¿Cómo se divide sin romper la coherencia de la feature?

### La solución: stacked PRs

Es el patrón documentado y usado en Meta, Google y la mayoría de empresas grandes. Cada PR es deployable por sí solo. La feature end-to-end emerge cuando todos se mergean en orden.

**Ejemplo:** "Sistema de login con Google OAuth" (estimado 2500 LOC)

```
PR #1  base: scaffolding             (250 LOC)
       └── Crea módulo auth/, schemas, config vacía
       └── Mergeable solo

PR #2  feature: oauth-flow           (400 LOC)  depende de #1
       └── Implementa OAuth handshake
       └── Mergeable solo

PR #3  feature: jwt-generation       (300 LOC)  depende de #2
       └── Genera y firma JWT
       └── Mergeable solo

PR #4  feature: protected-routes     (350 LOC)  depende de #3
       └── Middleware que valida JWT
       └── Mergeable solo

PR #5  feature: frontend-button       (200 LOC)  depende de #2
       └── Botón "Login con Google" en UI
       └── Mergeable solo

PR #6  feature: tests-integration     (500 LOC)  depende de #1-#5
       └── Tests e2e de todo el flow
       └── Mergeable solo
```

Total: 2000 LOC en 6 PRs, ninguno mayor a 500 LOC.

### Reglas de los stacked PRs

1. Cada PR es deployable por sí solo (puede tener feature flag si no tiene sentido activarlo)
2. El orden importa: PR base primero, dependencias después
3. Se mergean en orden (PR #1 → #2 → #3...), uno por uno
4. Si la feature se cancela a mitad, lo mergeado queda, lo pendiente se descarta. No queda código muerto
5. El stack se puede reordenar con herramientas como Graphite

### Herramientas

- **Graphite** (graphite.dev): la más popular, integración con GitHub CLI
- **gh-stack** de Carlos Becker: open source
- **Spr** (spr.com): la herramienta comercial original
- **Phabricator Differential**: lo que usa Meta internamente
- **Gerrit**: lo que usa Google, con "chain" para PRs apilados

### Alternativas

**Feature flags** (LaunchDarkly, Unleash, Flagsmith):
- Mergeás el código a main, lo apagas con un flag
- Activás el flag en producción cuando esté listo
- Bueno para: features que no se pueden dividir en capas
- Malo para: flags que quedan prendidos para siempre

**Branch by Abstraction** (Jez Humble, Continuous Delivery):
- Introducís una abstracción nueva, migrás consumidores de a poco, borrás la abstracción vieja al final
- Bueno para: refactors grandes
- Malo para: features nuevas

**Trunk-Based Development** (Adam Tornhill):
- Todo a main, protegido por feature flags y tests
- PRs muy chicos, merge frecuente
- Bueno para: equipos maduros con buena cobertura de tests
- Malo para: equipos chicos

### Anti-patrones

- Mega-PR de 5000 LOC que se aprueba de una porque "total lo testeé yo"
- Acumular 15 PRs sin mergear esperando "tener todo listo"
- Dividir por archivo en vez de por capa funcional
- Mezclar refactor + feature en el mismo PR

### Política de división por tamaño

| Tamaño del cambio | Estrategia |
|---|---|
| <300 LOC | PR normal de 1 capa |
| 300-800 LOC | PR normal, con cuidado en el review |
| 800-2000 LOC | Stacked PRs obligatorio (2-4 PRs) |
| >2000 LOC | Stacked PRs + feature flags o repensar el diseño |

---

## Conteo de líneas en PRs (¿se cuentan los tests?)

### Las 3 posturas que existen

**Postura 1: "Se cuenta todo"** (Microsoft Research)
- El reviewer tiene que leerlo igual
- Ocupa el mismo espacio en pantalla
- El tiempo de review es el mismo

**Postura 2: "Solo código de producción"** (algunos equipos)
- Los tests son "más baratos de revisar" porque son repetitivos
- Excluirlos da una métrica más realista del esfuerzo real
- Problema: falsea la métrica si un PR tiene 100 LOC prod + 2000 LOC tests

**Postura 3: "Se cuentan por separado"** (Google, Meta, postura moderna)
- Dos métricas independientes: prod y tests
- Permite detectar PRs con mala cobertura de tests

### Qué dice cada fuente seria

| Fuente | Política |
|---|---|
| Microsoft Research (McIntosh 2016) | Cuenta todo el diff |
| Google Sadowski 2018 | Cuenta todo, pero reporta ratio test/prod |
| Facebook/Meta | Cuenta todo, pero usan herramientas para ignorar generados |
| Software Engineering at Google | Recomienda separar métricas, no mezclarlas |
| Your Code as a Crime Scene (Tornhill) | Cuenta cambios lógicos, no líneas |
| Conventional PR size guides | Suelen excluir tests y comentarios |

### El problema real

El paper de McIntosh encontró que los tests no siguen el mismo patrón que el código de prod:

```
PR chico  (<200 LOC prod):   test/prod ratio ~2-3× (más tests que código)
PR mediano (200-800 LOC):    test/prod ratio ~1-2×
PR grande  (>800 LOC):       test/prod ratio ~0.3× (menos tests por línea)
```

Cuando alguien manda un PR grande, suele mandar menos tests de los que debería. Un mega-PR de 3000 LOC con 300 LOC de tests es una bomba de tiempo.

### Política recomendada

```
Límite por PR:
- 500 LOC de producción
- 1500 LOC de tests
- 2000 LOC total

Ratio mínimo de tests vs prod:
- Bug fix:     0.5×
- Feature:     1.0×
- Refactor:    0.3×

Si un PR es solo tests: no tiene límite estricto (tests son baratos)
Si un PR es solo refactor: contar todo igual, refactor grande también es riesgo
```

### Formas de medir en la práctica

**A ojo (simple):**
```
"Tengo ~300 líneas de prod, ~200 de tests, total ~500 → OK"
```

**Script rápido:**
```bash
git diff main --stat
git diff main -- 'src/' | wc -l    # prod
git diff main -- 'tests/' | wc -l   # tests
```

**Pre-commit hook:**
```bash
PROD_LINES=$(git diff --cached -- 'src/' | grep -c '^+')
TEST_LINES=$(git diff --cached -- 'tests/' | grep -c '^+')

if [ $PROD_LINES -gt 500 ]; then
  echo "PR muy grande: $PROD_LINES líneas de prod (máx 500)"
  exit 1
fi
```

---

## Resumen ejecutivo

- **Sweet spot de tamaño:** 200-400 LOC. Máximo duro 2000 LOC total (500 prod + 1500 tests).
- **Para features grandes:** stacked PRs, no un mega-PR.
- **Tests se cuentan:** sí, pero por separado de prod. Un PR sin tests es un PR incompleto.
- **Regla de oro:** si el reviewer no puede leerlo entero, dividir.
