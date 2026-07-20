# Go

**Creado:** 19 Jul 2026
**Carpeta:** `go/`

Lenguaje compilado, estaticamente tipado, con goroutines y canales como modelo de concurrencia. Creado en Google (2007, anuncio publico 2009, v1.0 en 2012). Los autores son Rob Pike, Ken Thompson y Robert Griesemer — gente de Unix, Plan 9 y C.

---

## Filosofia central

> *"A little copying is better than a little dependency."* — Rob Pike

- Simplicidad como feature (no hay herencia, no hay excepciones, no hay generics hasta 2022).
- `gofmt` reforma tu codigo por ti — el formateador canonico es el oficial, no se discute.
- `go build` en segundos. El compilador es tu amigo.
- Concurrencia con goroutines y canales (modelo CSP de Hoare, 1978).
- Composicion sobre herencia, interfaces satisfechas implicitamente.
- Backward compatibility sagrada — codigo Go 1.0 sigue compilando en Go 1.22+.

---

## Carpetas del tema

| Carpeta | Descripcion |
|---|---|
| [fundamentos/](./fundamentos/) | Origenes, filosofia, cuando usarlo, instalacion, primer hola mundo |
| [sintaxis/](./sintaxis/) | Variables, funciones, control de flujo, tipos, interfaces basicas |
| [estructuras-de-datos/](./estructuras-de-datos/) | Arrays, slices, maps, structs, punteros — como Go los modela distinto a otros lenguajes |
| [concurrencia/](./concurrencia/) | Goroutines, canales, select, sync package, el modelo CSP |
| [errores-y-panics/](./errores-y-panics/) | Idiomatica: error como valor, panic/recover, defer, wrapping con %w |
| [testing/](./testing/) | testing package, table-driven tests, benchmarks, fuzzing, coverage |
| [web-y-http/](./web-y-http/) | net/http, routers (chi, gin, echo), middleware, templates, websockets |
| [bases-de-datos/](./bases-de-datos/) | database/sql, drivers (pgx, mysql), ORM (gorm, sqlc), migrations, context |
| [herramientas-y-ecosistema/](./herramientas-y-ecosistema/) | go tool, go vet, gofmt, go modules, GOPATH, linters, debuggers |
| [proyectos/](./proyectos/) | Proyectos completos aplicando todo lo aprendido |

---

## Roadmap sugerido (autoestudio, sin prisa)

1. **fundamentos/** — origenes, instalacion, primer programa, go tool basico
2. **sintaxis/** — variables, funciones, control de flujo, tipos
3. **estructuras-de-datos/** — slices, maps, structs, punteros (importante entender slices a fondo)
4. **errores-y-panics/** — error handling idiomatico antes de meterse con concurrencia
5. **testing/** — el testing es parte del stdlib, aprenderlo temprano paga
6. **herramientas-y-ecosistema/** — go modules, go vet, golangci-lint, delve
7. **concurrencia/** — goroutines, canales, select, sync. Esto es lo que hace a Go Go.
8. **web-y-http/** — net/http, despues chi/gin. Una API REST basica.
9. **bases-de-datos/** — database/sql, despues pgx, despues sqlc
10. **proyectos/** — aqui se aplica todo: CLI tool + API REST + algo con DB

---

## Recursos externos

- [go.dev](https://go.dev) — sitio oficial
- [go.dev/talks](https://go.dev/talks/) — videos y slides de Rob Pike, Russ Cox, etc.
- [go.dev/doc/effective_go](https://go.dev/doc/effective_go) — como escribir Go idiomatico
- [gobyexample.com](https://gobyexample.com) — ejemplos cortos, ideal para consultar rapido
- [pkg.go.dev](https://pkg.go.dev) — documentacion de la stdlib y cualquier modulo
- "The Go Programming Language" — Donovan & Kernighan — LA biblia

---

*Documenta tu aprendizaje sobre Go — desde los origenes hasta proyectos reales.*
