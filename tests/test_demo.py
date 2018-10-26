import pytest

from demo.jwt import IdentityMaker, JwtIdentityPolicy, JwtAuthPolicy
from security_interface.api import Security

SECRET = "SECRET"

identity_maker = IdentityMaker(expired_after=1, secret=SECRET)

jwt_identity = JwtIdentityPolicy(secret=SECRET)
jwt_auth = JwtAuthPolicy()

security = Security(jwt_identity, jwt_auth)


@pytest.mark.asyncio
async def test_jwt_demo():
    payload = {"login": "Bakhtiyor", "scope": ["read", "write"]}

    token = identity_maker.make(payload)

    identity = await security.check_authorized(token)
    assert "Bakhtiyor" == identity["login"]
    assert await security.can(token, "read")
    assert await security.can(token, "write")
    assert not await security.can(token, "private")
