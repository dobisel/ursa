from os.path import dirname, join

from restfulpy.application import Application

from ursa.authentication import Authenticator
from ursa.controllers import Root
from ursa import basedata

__version__ = '0.1.0-dev.0'


class Ursa(Application):
    __authenticator__ = Authenticator()

    builtin_configuration = """
    db:
      url: postgresql://postgres:postgres@localhost/ursa_dev
      test_url: postgresql://postgres:postgres@localhost/ursa_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres
      echo: false

    application:
      welcome_url: http://localhost:8081/welcome
    
    network:
      interfaces_dir: %(data_dir)s
      interfaces_file: %(data_dir)s/interfaces
      default_interface: eth0
    """

    def __init__(self):
        super().__init__(
            self.__class__.__name__.lower(),
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    def insert_mockup(self):
        print('No mockup data.')

    def insert_basedata(self):  # pragma: no cover
        basedata.insert()


ursa = Ursa()
