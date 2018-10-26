import logging
import time

from security_interface import IdentityPolicyInterface, AuthorizationPolicyInterface

try:
    import jwt
except ImportError:
    jwt = None

__all__ = ["IdentityMaker", "JwtAuthPolicy", "JwtIdentityPolicy"]


class IdentityMaker:
    def __init__(self, expired_after, secret, algorithm="HS256"):
        self.expired_after = expired_after
        self.secret = secret
        self.algorithm = algorithm
        if jwt is None:
            raise TypeError("Please install PyJWT")

    def make(self, payload: dict) -> str:
        payload.update(
            {
                "exp": int(time.time() + self.expired_after),
                "ait": int(time.time()),
                "scope": payload.get("scope", []),
            }
        )

        return jwt.encode(payload, self.secret, algorithm=self.algorithm)


class JwtIdentityPolicy(IdentityPolicyInterface):
    def __init__(self, secret, algorithm="HS256"):
        self.algorithm = algorithm
        self.secret = secret

    async def identify(self, identity):
        if jwt is None:
            raise TypeError("Please install PyJWT")
        try:
            return jwt.decode(
                identity,
                self.secret,
                algorithms=[self.algorithm],
                options={"verify_exp": True, "verify_iat": True},
            )
        except Exception as e:
            logging.error("Error during read token: {}".format(e))
            return None


class JwtAuthPolicy(AuthorizationPolicyInterface):
    async def can(self, identity, permission):
        return permission in identity["scope"]
