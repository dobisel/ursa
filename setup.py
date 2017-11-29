
import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'ursa', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


dependencies = [
    'nanohttp >= 0.20.1',
    'pyjwt',
    'idna <2.6, >=2.5',

    # Deployment
    'gunicorn',
]


setup(
    name="koala",
    version=package_version,
    author="Mehrdad Pedramfar",
    author_email="mehrdad@carrene.com",
    install_requires=dependencies,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ursa = ursa:ursa.cli_main'
        ]
    }
)