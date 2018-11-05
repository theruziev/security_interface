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
        """
        Return the claimed identity or
        ``None`` if check is failed.

        :param identity: Claim
        :return: Checked identity or ``None`` if check is failed.
        """
        identify = await self.identity_policy.identify(identity)
        return identify

    async def can(self, identity, permission) -> bool:
        """
        Check user permissions.

        :return: ``True`` if the identity is allowed the permission, else return ``False``.
        """
        assert isinstance(permission, (str, enum.Enum)), permission
        assert permission
        identify = await self.identity_policy.identify(identity)
        # non-registered user still may has some permissions
        access = await self.autz_policy.can(identify, permission)
        return access

    async def is_anonymous(self, identity) -> bool:
        """

        :param identity: Claim
        :return: ``True`` if user anonymous otherwise ``False``
        """
        identify = await self.identity_policy.identify(identity)
        if identify is None:
            return True
        return False

    async def check_authorized(self, identity):
        """
        Works like :func:`Security.identity`, but when check is failed
        :func:`UnauthorizedError` exception is raised.

        :param identity: Claim
        :return: Checked claim or return ``None``
        :raise: :func:`UnauthorizedError`
        """
        identify = await self.identify(identity)
        if identify is None:
            raise UnauthorizedError()
        return identify

    async def check_permission(self, identity, permission):
        """
        Works like :func:`Security.can`, but when check is failed
        :func:`ForbiddenError` exception is raised.

        :param identity: Claim
        :param permission: Permission
        :return: Checked claim
        :raise: :func:`ForbiddenError`
        """
        await self.check_authorized(identity)
        allowed = await self.can(identity, permission)
        if not allowed:
            raise ForbiddenError()
