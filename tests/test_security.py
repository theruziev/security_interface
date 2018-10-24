import logging
import jwt
import pytest

from security_interface import AuthorizationPolicyInterface, IdentityPolicyInterface
from security_interface.api import Security
from security_interface.exceptions import ForbiddenError, UnauthorizedError

SECRET = "secret"


class JWTIdentityPolicy(IdentityPolicyInterface):
    def __init__(self, secret, algorithm="HS256"):
        if jwt is None:
            raise RuntimeError("Please install `PyJWT`")
        self.secret = secret
        self.algorithm = algorithm

    async def identify(self, identity):
        try:
            identity = jwt.decode(identity, self.secret, algorithms=[self.algorithm])
            return identity
        except Exception as e:
            logging.error("Error during read identity: {}".format(e))
            return None


class Autz(AuthorizationPolicyInterface):
    async def can(self, identity, permission):
        return permission in identity["scope"]


@pytest.fixture
def make_token():
    def factory(payload, secret):
        return jwt.encode(payload, secret, algorithm="HS256")

    return factory


security = Security(JWTIdentityPolicy(secret=SECRET), Autz())


@pytest.mark.asyncio
async def test_identify(make_token):
    identity_raw = {"login": "Bakhtiyor", "scope": ["read", "write", "private"]}
    token = make_token(identity_raw, SECRET)

    identity = await security.identify(token)
    assert "Bakhtiyor" == identity["login"]
    assert await security.can(token, "read")
    assert await security.can(token, "write")
    assert await security.can(token, "private")
    assert not await security.can(token, "non_exist_in_scope")
    assert "Bakhtiyor" == (await security.check_authorized(token))["login"]

    #  Wrong cases
    wrong_token = make_token(identity_raw, "WRONG_SECRET")

    with pytest.raises(UnauthorizedError):
        await security.check_authorized(wrong_token)
        await security.check_permission(wrong_token, "read")

    with pytest.raises(ForbiddenError):
        await security.check_permission(token, "non_exist_in_scope")
