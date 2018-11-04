.. image:: https://img.shields.io/travis/com/bruziev/security_interface.svg?style=flat-square
        :target: https://travis-ci.com/bruziev/security_interface
.. image:: https://img.shields.io/codecov/c/github/bruziev/security_interface.svg?style=flat-square
        :target: https://codecov.io/gh/bruziev/security_interface
.. image:: https://img.shields.io/pypi/v/security_interface.svg?style=flat-square
        :alt: PyPI
        :target: https://pypi.org/project/security-interface/

Security Interface
==================

This library provides easy API for authentication and authorization.

Installation
------------

Install with the following command::

    $ pip install security_interface


Usage
-----

First of all you need implement ``IdentityPolicyInterface``
and ``AuthorizationPolicyInterface`` interfaces. For example we can implement JWT Security::

   import jwt
   from security_interface import IdentityPolicyInterface, AuthorizationPolicyInterface

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
               return None

   class JwtAuthPolicy(AuthorizationPolicyInterface):
       async def can(self, identity, permission):
           return permission in identity["scope"]


Create security instance with our implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

   from security_interface.api import Security
   jwt_identity = JwtIdentityPolicy("SECRET")
   jwt_auth_policy = JwtAuthPolicy()
   security = Security(jwt_identity, jwt_auth_policy)
   # Checking claim
   security.identify(CLAIM)
   # Checking permission
   security.can(CLAIM, "read")
   security.can(CLAIM, "write")

For full implementation see `DEMO <https://github.com/bruziev/security_interface/tree/master/demo>`_
