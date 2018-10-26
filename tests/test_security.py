import logging
import pytest

from security_interface import AuthorizationPolicyInterface, IdentityPolicyInterface
from security_interface.api import Security
from security_interface.exceptions import ForbiddenError, UnauthorizedError

SECRET = "secret"


class TestIdentityPolicy(IdentityPolicyInterface):
    async def identify(self, identity):
        return identity


class Autz(AuthorizationPolicyInterface):
    async def can(self, identity, permission):
        return permission in identity["scope"]


security = Security(TestIdentityPolicy(), Autz())


@pytest.mark.asyncio
async def test_identify():
    identity_raw = {"login": "Bakhtiyor", "scope": ["read", "write", "private"]}

    identity = await security.identify(identity_raw)
    assert "Bakhtiyor" == identity["login"]

    assert await security.can(identity_raw, "read")
    assert await security.can(identity_raw, "write")
    assert await security.can(identity_raw, "private")
    assert not await security.can(identity_raw, "non_exist_in_scope")

    try:
        await security.check_permission(identity_raw, "read")
        await security.check_permission(identity_raw, "write")
        await security.check_permission(identity_raw, "private")
    except ForbiddenError as e:
        assert False, str(e)

    with pytest.raises(ForbiddenError):
        await security.check_permission(identity_raw, "non_exist_in_scope")

    assert "Bakhtiyor" == (await security.check_authorized(identity_raw))["login"]

    # Wrong cases
    with pytest.raises(UnauthorizedError):
        await security.check_authorized(None)
        await security.check_permission(None, "read")

    with pytest.raises(ForbiddenError):
        await security.check_permission(identity_raw, "non_exist_in_scope")

    # Test Anonymous
    assert await security.is_anonymous(None)
    assert not await security.is_anonymous(identity_raw)
