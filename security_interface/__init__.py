import abc


class IdentityPolicyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def identify(self, identity):
        """Return the claimed identity of the user associated request or
        ``None`` if no identity can be found associated with the request."""
        pass  # pragma: no cover


class AuthorizationPolicyInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def can(self, identity, permission):
        """Check user permissions.

        Return True if the identity is allowed the permission in the
        current context, else return False.
        """
        pass  # pragma: no cover
