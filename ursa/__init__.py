from os.path import dirname, join

from restfulpy.application import Application

from ursa.authentication import Authenticator
from ursa.controllers import Root
from .mockup_data import insert_mockup

__version__ = '0.1.0-planning.0'


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
        insert_mockup()

    def insert_basedata(self):  # pragma: no cover
        print('This project doesn\'t have any base-data.')


ursa = Ursa()
