import abc


class IdentityPolicyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def identify(self, identity):
        """
        You need return the checked claimed identity or
        ``None`` if check is fail.

        :param identity: Claim
        :return: Checked ``identity`` or ``None`` if check is failed.
        """
        pass  # pragma: no cover


class AuthorizationPolicyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def can(self, identity, permission):
        """
        You need to implement checking permission.

        :return: ``True`` if the identity is allowed the permission, else return ``False``.
        """
        pass  # pragma: no cover
