# 01 — Origenes y Filosofia de Go

**Creado:** 19 Jul 2026
**Carpeta:** `fundamentos/`

---

## Contexto historico

Go nace en **Google alrededor de 2007** y se anuncia publicly en **noviembre de 2009**. La version 1.0 sale en **marzo de 2012**.

Los autores originales son tres figuras pesadas:

| Persona | Rol en Go | Antes / despues |
|---|---|---|
| **Robert Griesemer** | Co-autor | V8 (motor JS de Chrome), Java HotSpot, Sawzall |
| **Rob Pike** | Co-autor | Plan 9, UTF-8, co-creador de Limbo, libs de Unix en Bell Labs |
| **Ken Thompson** | Co-autor | Co-creador de Unix, co-creador de C, inventor de UTF-8, Plan 9, B |

Despues se sumo **Ian Lance Taylor** (gccgo) y **Russ Cox** (quien tomo las riendas del lenguaje y el ecosistema de modulos).

## El problema que venian sufriendo

A mediados de los 2000 Google crecio brutalmente:

- **Millones de lineas de codigo** en un unico monorepo (su `google3`).
- Builds **lentisimos** — esperar minutos para compilar un cambio pequeno.
- **Dependencias imposibles** — C/C++ con `#include` se volvio inmanejable a esa escala.
- Multiprocesadores到处都是 (multicore era ya lo normal) pero C/C++/Java no lo hacian facil.
- **Frustracion con la complejidad**: C++ se sentia como un lenguaje que crecia sin direccion. Java arrastraba baggage de los 90.
- Codigo nuevo en lenguajes dinamicos (Python, JS) escalaba mal en performance y en equipos grandes.

Necesitaban algo con la **eficiencia de C++**, la **legibilidad de un lenguaje dinamico**, y tooling de primera (build, test, format, deps) **incluido en el toolchain**, no como addons.

## La filosofia de Go (lo que el lenguaje cree)

Go es **opinionated**. Estas son las decisiones de diseno que definen su sabor:

1. **Simplicidad como feature, no como limitacion** — "~25 keywords, no mas". No hay generics hasta 2022, no hay herencia, no hay excepciones, no hay macros. La idea: menos conceptos = menos formas de equivocarse.
2. **Una sola forma obvia de hacer las cosas** — el `gofmt` reformatea tu codigo por ti. No debates sobre tabs vs espacios, donde va la llave, etc. El formateador CANONICO es el oficial.
3. **El compilador es tu amigo** — `go build` es increiblemente rapido (segundos, no minutos), error messages son utiles y apuntan a la linea exacta y a veces sugieren el fix. El tooling **es** el lenguaje.
4. **Concurrencia es ciudadana de primera** — `go f()` lanza una goroutine, `ch <- valor` manda por un canal. El modelo CSP de Hoare (Communicating Sequential Processes, 1978) hecho facil.
5. **Composicion sobre herencia** — no hay clases, hay `struct` con metodos. Interfaces son **satisfied implicitly** (no declaras `implements`). Si camina como pato y hace cuac, es pato.
6. **Backward compatibility es sagrada** — el [Go 1 Compatibility Promise](https://go.dev/doc/go1compat) garantiza que codigo escrito en Go 1.0 sigue compilando en Go 1.22+. Solo hubo 2 breaking changes historicas, ambos menores.
7. **Batteries included** — `net/http`, `encoding/json`, `testing`, `crypto/tls`, `compress/gzip`, todo en stdlib. Para una API REST basica no necesitas ningun framework externo.
8. **Errores son valores, no excepciones** — `if err != nil { return err }` se repite 1000 veces. Es feo y verboso, pero es **explicito** y **local**. Sabes exactamente donde puede fallar una funcion sin leer un try/catch lejanos.
9. **Codigo es para humanos primero** — la legibilidad pesa mas que la cleverness. Rob Pike: *"A little copying is better than a little dependency."*
10. **El garbage collector mejoro sin parar** — en 2007 los GC eran lentos, en 2024 son pausas sub-milisegundo. Go demostro que un GC moderno no es excusa para C++.

## Que tipo de programas se escriben en Go

Go brilla en:

- **Servicios de red / APIs / microservicios** — es donde nacio. `net/http` es solido, soporta HTTP/2 nativamente.
- **CLI tools** — Docker, kubectl, terraform, gh, hugo, fzf (originalmente), todas las herramientas modernas del dev. Un solo binario estatico, sin dependencias, lo instalas y funciona.
- **Infraestructura cloud** — Kubernetes, Docker, Prometheus, Consul, Vault, Terraform, etcd. Casi todo el "cloud native" corre en Go.
- **Servicios de backend con mucha concurrencia** — scrapers, proxies, message brokers, gateways.
- **DevOps tooling** — scripts que necesitas que sean rapidos y portables.

Go NO es ideal para:

- **GUI desktop** — el ecosistema es pobre. Mejor Electron, Tauri, Qt.
- **Machine learning / data science** — Python manda. Go tiene bindings pero no es su fuerte.
- **Mobile nativo** — aunque existe gomobile, no es mainstream.
- **Sistemas embebidos hard real-time** — el GC introduce pausas impredecibles. Rust o C mejor.
- **Aplicaciones donde necesitas zero-cost abstractions** — Rust gana por su sistema de tipos.

## Curiosidades que vale la pena saber

- El **mascota** es el Go gopher, dibujado por Renee French (la misma que hizo el poster de Unix "uriel" de Plan 9). Es de dominio publico — por eso lo ves en todas partes.
- El nombre **"Go"** es porque era corto y facil de googlear. Pero "go" es tambien palabra reservada en muchos lenguajes, asi que crearon el dominio **golang.org** para SEO. Por eso mucha gente le dice "golang" aunque el lenguaje se llama Go.
- El **disenador principal del GC** desde 2018 es **Austin Clements**, quien mantiene su propio blog tecnico excelente.
- Go **no tiene un "Hello World" oficial** del lenguaje en si, pero `package main; import "fmt"; func main() { fmt.Println("Hello, 世界") }` muestra algo de UTF-8 nativo.
- La mascota es tan popular que hay una cancion oficial: *"The Go Gopher Song"*.

## Donde profundizar (recursos)

| Recurso | Tipo | Para que sirve |
|---|---|---|
| go.dev/talks | Videos + slides oficiales | Escuchar a Rob Pike y cia explicar las decisiones |
| go.dev/doc/effective_go | Documento oficial | El "como escribir Go idiomatico" canonico |
| github.com/golang/go/wiki/CodeReviewComments | Wiki | Comentarios de code review del equipo de Go |
| "The Go Programming Language" — Donovan & Kernighan | Libro | LA biblia. Brian Kernighan (el de "C Programming Language") co-escribio esto |
| "Concurrency in Go" — Katherine Cox-Buday | Libro | Solo concurrencia, profunda |
| gobyexample.com | Web | Ejemplos cortos, ideal para consultar rapido |

---

*Proximo: 02-instalacion-y-primer-hola-mundo.md — instalamos Go, configuramos GOPATH, escribimos y compilamos el primer programa.*
