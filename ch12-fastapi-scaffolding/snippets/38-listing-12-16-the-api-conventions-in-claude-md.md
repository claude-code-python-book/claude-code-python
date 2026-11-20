## API conventions
- Create returns 201 with a `Location` header. List endpoints take
  `limit` (1 to 100, default 20) and `offset`, and return `Page[...]`.
- The customer comes from the token (`CurrentUser`), never from the
  request body or query.
- The service raises `OrderError` subclasses, never `HTTPException`.
  Map each new error in `EXCEPTION_HANDLERS`. Error bodies are RFC 9457
  problem details.
- Request models set `extra="forbid"`. Money is `Decimal` with two
  places; JSON carries it as a string.
- Every path operation has a `summary`, a return type, and `responses`
  for each error status it can return.
