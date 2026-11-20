# Chapter 12 — FastAPI Scaffolding: Generate a Production-Ready API Fast

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`ch12-sample`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-terminal.sh`](snippets/01-terminal.sh) | Terminal | bash | 2. The Running Example: An Orders Service |
| [`02-code.toml`](snippets/02-code.toml) | Code | toml | 2. The Running Example: An Orders Service |
| [`03-terminal.sh`](snippets/03-terminal.sh) | Terminal | bash | 2. The Running Example: An Orders Service |
| [`04-prompt.txt`](snippets/04-prompt.txt) | Prompt | prompt | 2. The Running Example: An Orders Service |
| [`05-listing-12-1-the-orders-service-package.txt`](snippets/05-listing-12-1-the-orders-service-package.txt) | Listing 12-1: The orders-service package | text | 2. The Running Example: An Orders Service |
| [`06-prompt.txt`](snippets/06-prompt.txt) | Prompt | prompt | 3. Scaffolding Pydantic v2 Schemas |
| [`07-listing-12-2-request-models-in-src-orders-schemas-py.py`](snippets/07-listing-12-2-request-models-in-src-orders-schemas-py.py) | Listing 12-2: Request models in src/orders/schemas.py | python | 3. Scaffolding Pydantic v2 Schemas |
| [`08-output.txt`](snippets/08-output.txt) | Output | text | 3. Scaffolding Pydantic v2 Schemas |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 3. Scaffolding Pydantic v2 Schemas |
| [`10-listing-12-3-response-models-in-src-orders-schemas-py.py`](snippets/10-listing-12-3-response-models-in-src-orders-schemas-py.py) | Listing 12-3: Response models in src/orders/schemas.py | python | 3. Scaffolding Pydantic v2 Schemas |
| [`11-code.json`](snippets/11-code.json) | Code | json | 3. Scaffolding Pydantic v2 Schemas |
| [`12-output.txt`](snippets/12-output.txt) | Output | text | 3. Scaffolding Pydantic v2 Schemas |
| [`13-output.txt`](snippets/13-output.txt) | Output | text | 3. Scaffolding Pydantic v2 Schemas |
| [`14-prompt.txt`](snippets/14-prompt.txt) | Prompt | prompt | 4. Routers, Path Operations, and Status Codes |
| [`15-listing-12-4-the-first-half-of-src-orders-api-orders-py.py`](snippets/15-listing-12-4-the-first-half-of-src-orders-api-orders-py.py) | Listing 12-4: The first half of src/orders/api/orders.py | python | 4. Routers, Path Operations, and Status Codes |
| [`16-listing-12-5-a-first-draft-that-ruff-s-fastapi-rules-rejec.py`](snippets/16-listing-12-5-a-first-draft-that-ruff-s-fastapi-rules-rejec.py) | Listing 12-5: A first draft that Ruff's FastAPI rules reject | python | 4. Routers, Path Operations, and Status Codes |
| [`17-output.txt`](snippets/17-output.txt) | Output | text | 4. Routers, Path Operations, and Status Codes |
| [`18-listing-12-6-providers-and-aliases-in-src-orders-deps-py.py`](snippets/18-listing-12-6-providers-and-aliases-in-src-orders-deps-py.py) | Listing 12-6: Providers and aliases in src/orders/deps.py | python | 5. Dependency Injection with Depends |
| [`19-prompt.txt`](snippets/19-prompt.txt) | Prompt | prompt | 6. The Service and Repository Layers |
| [`20-listing-12-7-two-methods-of-orderservice-in-src-orders-ser.py`](snippets/20-listing-12-7-two-methods-of-orderservice-in-src-orders-ser.py) | Listing 12-7: Two methods of OrderService in src/orders/service.py | python | 6. The Service and Repository Layers |
| [`21-listing-12-8-the-repository-interface-in-src-orders-reposi.py`](snippets/21-listing-12-8-the-repository-interface-in-src-orders-reposi.py) | Listing 12-8: The repository interface in src/orders/repository.py | python | 6. The Service and Repository Layers |
| [`22-output.txt`](snippets/22-output.txt) | Output | text | 6. The Service and Repository Layers |
| [`23-listing-12-9-src-orders-handlers-py.py`](snippets/23-listing-12-9-src-orders-handlers-py.py) | Listing 12-9: src/orders/handlers.py | python | 7. Validation, Exception Handlers, and Error Responses |
| [`24-output.txt`](snippets/24-output.txt) | Output | text | 7. Validation, Exception Handlers, and Error Responses |
| [`25-listing-12-10-src-orders-config-py.py`](snippets/25-listing-12-10-src-orders-config-py.py) | Listing 12-10: src/orders/config.py | python | 8. Settings and Environments with pydantic-settings |
| [`26-output.txt`](snippets/26-output.txt) | Output | text | 8. Settings and Environments with pydantic-settings |
| [`27-listing-12-11-src-orders-tokens-py.py`](snippets/27-listing-12-11-src-orders-tokens-py.py) | Listing 12-11: src/orders/tokens.py | python | 9. Authentication: OAuth2 and JWT |
| [`28-output.txt`](snippets/28-output.txt) | Output | text | 9. Authentication: OAuth2 and JWT |
| [`29-listing-12-12-authenticate-in-src-orders-users-py.py`](snippets/29-listing-12-12-authenticate-in-src-orders-users-py.py) | Listing 12-12: authenticate() in src/orders/users.py | python | 9. Authentication: OAuth2 and JWT |
| [`30-output.txt`](snippets/30-output.txt) | Output | text | 9. Authentication: OAuth2 and JWT |
| [`31-listing-12-13-src-orders-middleware-py.py`](snippets/31-listing-12-13-src-orders-middleware-py.py) | Listing 12-13: src/orders/middleware.py | python | 10. Middleware, CORS, and Request Logging |
| [`32-output.txt`](snippets/32-output.txt) | Output | text | 10. Middleware, CORS, and Request Logging |
| [`33-output.txt`](snippets/33-output.txt) | Output | text | 10. Middleware, CORS, and Request Logging |
| [`34-listing-12-14-src-orders-app-py.py`](snippets/34-listing-12-14-src-orders-app-py.py) | Listing 12-14: src/orders/app.py | python | 11. OpenAPI Docs as the API Contract |
| [`35-listing-12-15-tests-api-conftest-py-and-the-first-api-test.py`](snippets/35-listing-12-15-tests-api-conftest-py-and-the-first-api-test.py) | Listing 12-15: tests/api/conftest.py and the first API test | python | 12. Tests at Every Layer |
| [`36-code.py`](snippets/36-code.py) | Code | python | 12. Tests at Every Layer |
| [`37-output.txt`](snippets/37-output.txt) | Output | text | 12. Tests at Every Layer |
| [`38-listing-12-16-the-api-conventions-in-claude-md.md`](snippets/38-listing-12-16-the-api-conventions-in-claude-md.md) | Listing 12-16: The API conventions in CLAUDE.md | markdown | 13. Patterns That Keep Scaffolding Consistent Across a Team |
| [`39-listing-12-17-claude-skills-new-endpoint-skill-md.md`](snippets/39-listing-12-17-claude-skills-new-endpoint-skill-md.md) | Listing 12-17: .claude/skills/new-endpoint/SKILL.md | markdown | 13. Patterns That Keep Scaffolding Consistent Across a Team |
