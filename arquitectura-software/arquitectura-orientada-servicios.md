# Arquitectura Orientada a Servicios

> Siempre debe existir un contrato para que un cliente se pueda conectar a un servidor. Este contrato dictará a dónde y con quién puede conectarse.

---

## El concepto central: contratos

En esta arquitectura, todo gira alrededor de un **contrato** entre el cliente y el servidor. El cliente no se conecta libremente — envía un contrato que dicta:

- A qué servidores puede conectarse
- Cómo debe ser la comunicación
- Qué operaciones están disponibles

Sin un contrato válido, no hay conexión. Todo o nada.

---

## SOAP — El contrato estricto

**SOAP** (Simple Object Access Protocol) es el estándar más riguroso dentro de las arquitecturas orientadas a servicios.

### Características

- **XML** como lenguaje de intercambio — todo se estructura en etiquetas XML
- **WSDL** (Web Services Description Language) como el manual de reglas — describe operaciones, tipos de datos, endpoints y bindings
- La conexión solo se da si el contrato enviado está **100% correcto** — una firma mal, algo mal escrito, y todo falla
- Contratos extremadamente detallados y predecibles

### Por qué sigue vivo

A pesar de ser considerado "viejo" y "burocrático", SOAP sigue siendo muy usado en sistemas donde la seguridad y la conformidad contractual son críticas:

- Sistemas financieros (bancos, bolsas)
- Salud (historias clínicas, seguros)
- Gobierno (trámites, certificaciones)
- Cualquier sistema donde un error de formato pueda tener consecuencias legales o financieras

Su rigidez no es una debilidad — es su fortaleza. Cuando necesitas garantías de que el mensaje queenvías es exactamente el mensaje que el receptor espera, SOAP entrega eso.

---

## OpenAPI — El contrato moderno en REST

**OpenAPI Specification (OAS)** es el estándar que rige cómo se escribe una API REST moderna. Es el equivalente moderno del contrato en SOAP.

OpenAPI dicta las reglas de cómo debe estructurarse una API:

- Endpoints disponibles
- Métodos HTTP permitidos
- Formato de request y response
- Autenticación requerida
- Tipos de datos
- Ejemplos de uso

REST API es el hijo moderno que sigue estas reglas de contrato.

---

## Swagger y OpenAPI — No son lo mismo

Esta es la distinción correcta:

| Nombre | Qué es |
|---|---|
| **OpenAPI Specification** | La especificación formal (versiones 3.0, 3.1) — el estándar en sí |
| **Swagger** | El ecosistema de herramientas de SmartBear que implementa ese estándar |
| **Swagger UI** | Visor web para explorar e interactuar con una API documentada con OpenAPI |
| **Swagger Editor** | Editor en navegador para escribir contratos OpenAPI |
| **Swagger Codegen** | Genera código cliente o servidor desde un contrato OpenAPI |

### La historia

1. **Swagger** fue creado por SmartBear como especificación para describir APIs REST
2. **En 2016**, SmartBear donó la especificación a la Linux Foundation y se-renombró a **OpenAPI Specification**
3. Hoy Swagger sigue existiendo como nombre comercial de las herramientas, pero el estándar se llama OpenAPI

### Analogía

- **WSDL** = el contrato completo en SOAP (describe todo: operaciones, tipos, bindings)
- **OpenAPI** = el contrato en REST moderno (la especificación formal)
- **Swagger** = las herramientas que implementan y visualizan ese contrato

Swagger UI es el visor moderno que permite ver una API documentada con OpenAPI y probarla desde el navegador.

---

## La regla inquebrantable

En una arquitectura orientada a servicios:

> **Sin contrato, no hay comunicación.** El contrato es la ley. Se cumple o no se conecta.

Esto aplica tanto para SOAP (donde el contrato es un documento WSDL) como para REST con OpenAPI (donde el contrato es el documento OpenAPI/JSON o YAML).