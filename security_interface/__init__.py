import abc


class IdentityPolicyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def identify(self, identity):
        """
        Return the claimed identity of the user associated request or
        ``None`` if no identity can be found associated with the request.

        :param identity: Claim
        :return: Return checked identity or ``None`` if check is failed.
        """
        pass  # pragma: no cover


class AuthorizationPolicyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def can(self, identity, permission):
        """
        Check user permissions.

        :return: Return ``True`` if the identity is allowed the permission, else return ``False``.
        """
        pass  # pragma: no cover
