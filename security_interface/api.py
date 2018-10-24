import enum

from .exceptions import UnauthorizedError, ForbiddenError
from . import IdentityPolicyInterface, AuthorizationPolicyInterface


class Security:
    def __init__(
        self, identity_policy: IdentityPolicyInterface, autz_policy: AuthorizationPolicyInterface
    ):
        self.identity_policy = identity_policy
        self.autz_policy = autz_policy

    async def identify(self, identity):
        identify = await self.identity_policy.identify(identity)
        return identify

    async def can(self, identity, permission):
        assert isinstance(permission, (str, enum.Enum)), permission
        assert permission
        identify = await self.identity_policy.identify(identity)
        # non-registered user still may has some permissions
        access = await self.autz_policy.can(identify, permission)
        return access

    async def is_anonymous(self, identity):

        identify = await self.identity_policy.identify(identity)
        if identify is None:
            return True
        return False

    async def check_authorized(self, identity):
        identify = await self.identify(identity)
        if identify is None:
            raise UnauthorizedError()
        return identify

    async def check_permission(self, request, permission):
        await self.check_authorized(request)
        allowed = await self.can(request, permission)
        if not allowed:
            raise ForbiddenError()
