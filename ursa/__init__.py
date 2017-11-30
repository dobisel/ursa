from os.path import dirname, join

from nanohttp.application import Application

from koala.controllers import Root
from koala.authentication import Authenticator
from .mockup_data import insert_mockup

__version__ = '0.1.0-planning.0'


class Koala(Application):
    # __authenticator__ = Authenticator()

    builtin_configuration = """
    db:
      uri: postgresql://postgres:postgres@localhost/ursa_dev
      test_uri: postgresql://postgres:postgres@localhost/ursa_test
      administrative_uri: postgresql://postgres:postgres@localhost/postgres
      echo: false

    application:
      welcome_url: http://localhost:8081/welcome

    """

    def __init__(self):
        super().__init__(
            self.__class__.__name__.lower(),
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

