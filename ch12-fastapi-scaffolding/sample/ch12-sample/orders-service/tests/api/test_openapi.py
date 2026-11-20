"""Check the parts of the OpenAPI schema that clients rely on."""

from fastapi import FastAPI


def test_the_contract_clients_depend_on(app: FastAPI) -> None:
    schema = app.openapi()
    paths = schema["paths"]
    assert {"201", "422"} <= set(paths["/orders"]["post"]["responses"])
    assert "404" in paths["/orders/{order_id}"]["get"]["responses"]
    assert {"404", "409"} <= set(
        paths["/orders/{order_id}/cancel"]["post"]["responses"]
    )
    security = schema["components"]["securitySchemes"]["OAuth2PasswordBearer"]
    assert security["type"] == "oauth2"
    assert "Problem" in schema["components"]["schemas"]
