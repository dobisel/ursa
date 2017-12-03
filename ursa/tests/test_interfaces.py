
import unittest
from os.path import join, dirname, abspath

from nanohttp import settings
from restfulpy.testing import FormParameter

from .helpers import WebTestCase, As


this_dir = abspath(dirname(__file__))
data_dir = join(this_dir, 'data')


class InterfaceTestCase(WebTestCase):
    url = '/apiv1/network/interfaces'

    @classmethod
    def configure_app(cls):
        super().configure_app()
        # TODO: Good file path
        settings.merge("""
        network: 
          interfaces_file: 
        """)

    def test_get(self):
        raise NotImplementedError()

    def test_put(self):
        self.login_as_admin()

        response, ___ = self.request(
            As.admin, 'PUT', f'{self.url}',
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('nameservers', '8.8.8.8 9.9.9.9'),
                FormParameter('network', '1.9.9.9'),
            ]
        )

        # TODO: Assert response
        # TODO: Assert the exact file


if __name__ == '__main__':
    unittest.main()
