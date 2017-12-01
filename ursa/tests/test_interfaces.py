
import unittest
from os.path import join, dirname, abspath

from restfulpy.testing import FormParameter

from .helpers import WebTestCase, As


this_dir = abspath(dirname(__file__))
data_dir = join(this_dir, 'data')


class InterfaceTestCase(WebTestCase):
    url = '/apiv1/network/interfaces'

    def test_get(self):
        pass

    def test_put(self):
        self.login_as_admin()

        response, ___ = self.request(
            As.admin, 'PUT', f'{self.url}',
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('DNS1', '8.8.8.8'),
                FormParameter('DNS2', '9.9.9.9'),
                FormParameter('network', '1.9.9.9'),
            ]
        )


if __name__ == '__main__':
    unittest.main()
