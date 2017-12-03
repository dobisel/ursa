
import unittest
from os.path import join, dirname, abspath

from nanohttp import settings
from restfulpy.testing import FormParameter
from network_interfaces import InterfacesFile

from ursa.tests.helpers import WebTestCase, As


this_dir = abspath(dirname(__file__))
data_dir = join(this_dir, 'data')


class InterfaceTestCase(WebTestCase):
    url = '/apiv1/network/interfaces'

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge("""
        network: 
          interfaces_file: %(data_dir)s/tests/interfaces
        """)

    def test_get(self):
        self.request(
            As.admin, 'GET', f'{self.url}',
            expected_status=401
        )

        self.login_as_admin()

        response, ___ = self.request(
            As.admin, 'GET', f'{self.url}'
        )

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface('eth0')

        self.assertEqual(response['address'], interface.address)
        self.assertEqual(response['netmask'], interface.netmask)
        self.assertEqual(response['gateway'], interface.gateway)
        self.assertEqual(response['nameServers'], interface.nameservers)
        self.assertEqual(response['networkId'], interface.network)

        self.logout()

    def test_put(self):

        self.request(
            As.admin, 'PUT', f'{self.url}',
            expected_status=401
        )

        self.request(
            As.admin, 'PUT', f'{self.url}',
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('nameServers', '8.8.8.8 9.9.9.9'),
                FormParameter('networkId', '1.9.9.9'),
            ],
            expected_status=401
        )

        self.login_as_admin()

        self.request(
            As.admin, 'PUT', f'{self.url}',
            expected_status=400
        )

        self.request(
            As.admin, 'PUT', f'{self.url}',
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255')
            ],
            expected_status=400
        )

        self.request(
            As.admin, 'PUT', f'{self.url}',
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('nameServers', '8.8.8.8 9.9.9.9'),
                FormParameter('networkId', None)
            ]
        )

        response, ___ = self.request(
            As.admin, 'PUT', f'{self.url}',
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('nameServers', '8.8.8.8 9.9.9.9'),
                FormParameter('networkId', '1.9.9.9'),
            ]
        )

        self.assertEqual(response['address'], '192.168.1.15')
        self.assertEqual(response['netmask'], '192.168.1.255')
        self.assertEqual(response['gateway'], '192.168.1.1')
        self.assertEqual(response['nameServers'], '8.8.8.8 9.9.9.9')
        self.assertEqual(response['networkId'], '1.9.9.9')

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface('eth0')

        self.assertEqual(interface.address, '192.168.1.15')
        self.assertEqual(interface.netmask, '192.168.1.255')
        self.assertEqual(interface.gateway, '192.168.1.1')
        self.assertEqual(interface.network, '1.9.9.9')
        self.assertEqual(interface.nameservers, '8.8.8.8 9.9.9.9')

        self.logout()


if __name__ == '__main__':
    unittest.main()
