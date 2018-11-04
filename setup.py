import setuptools
from setuptools import setup
from security_interface._version import __version__

setup(
    name='security_interface',
    version=__version__,
    url='https://github.com/bruziev/security_interface',
    license='MIT',
    author='Bakhtiyor Ruziev',
    author_email='bakhtiyor.ruziev@yandex.ru',
    description='Security Interface for you project.',
    long_description=open('README.rst').read().strip(),
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)
