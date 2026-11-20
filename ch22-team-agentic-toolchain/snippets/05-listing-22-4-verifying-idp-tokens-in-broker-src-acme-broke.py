class IdpTokenVerifier(TokenVerifier):
    """Accept RS256 JWTs from our IdP, minted for this broker, not expired."""

    def __init__(self, issuer: str, audience: str, resolve_key: KeyResolver) -> None:
        self.issuer, self.audience, self.resolve_key = issuer, audience, resolve_key

    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            claims = jwt.decode(
                token, self.resolve_key(token), algorithms=["RS256"],
                issuer=self.issuer, audience=self.audience,
                options={"require": ["exp", "iss", "aud", "sub"]},
            )
        except jwt.PyJWTError:
            return None                      # the SDK answers 401
        return AccessToken(
            token=token,
            client_id=claims.get("azp", "unknown"),
            scopes=claims.get("scope", "").split(),
            expires_at=claims["exp"],
            resource=self.audience,
            subject=claims["sub"],
            claims=claims,
        )
