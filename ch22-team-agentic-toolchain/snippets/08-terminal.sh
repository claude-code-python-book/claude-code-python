ACME_ID_TOKEN=$(acme-sso token --audience https://mcp.acme.example/mcp) \
    python -m acme_broker.register https://mcp.acme.example
