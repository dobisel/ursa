
import unittest
from os.path import join, dirname, abspath, exists
import os

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
        if exists(settings.network.interfaces_file):
            os.remove(settings.network.interfaces_file)

    def test_none_existing_interface(self):
        preserved_default_interface = settings.network.default_interface
        settings.network.default_interface = 'NotExistingInterface'
        self.login_as_admin()
        try:
            self.request(
                As.admin, 'GET', self.url,
                expected_status=409
            )
        finally:
            settings.network.default_interface = preserved_default_interface

    def test_get(self):
        # Logout to check anonymous access to interfaces file
        self.logout()
        self.request(
            As.anonymous, 'GET', self.url,
            expected_status=401
        )

        self.login_as_admin()

        response, ___ = self.request(
            As.admin, 'GET', self.url
        )

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface('eth0')

        self.assertEqual(response['address'], interface.address)
        self.assertEqual(response['netmask'], interface.netmask)
        self.assertEqual(response['gateway'], interface.gateway)
        self.assertEqual(response['broadcast'], interface.broadcast)
        self.assertEqual(response['nameServers'], interface['dns-nameservers'])
        self.assertEqual(response['networkId'], interface.network)

    def test_put(self):
        self.logout()
        self.request(
            As.anonymous, 'PUT', self.url,
            expected_status=401
        )

        self.request(
            As.anonymous, 'PUT', self.url,
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('broadcast', '192.168.1.255'),
                FormParameter('nameServers', '8.8.8.8 9.9.9.9'),
                FormParameter('networkId', '1.9.9.9'),
            ],
            expected_status=401
        )

        self.login_as_admin()

        self.request(
            As.admin, 'PUT', self.url,
            expected_status=400
        )

        self.request(
            As.admin, 'PUT', self.url,
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255')
            ],
            expected_status=400
        )

        self.request(
            As.admin, 'PUT', self.url,
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('broadcast', '192.168.1.255'),
                FormParameter('nameServers', '8.8.8.8 9.9.9.9'),
                FormParameter('networkId', '')
            ]
        )

        self.request(
            As.admin, 'PUT', self.url,
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('broadcast', '192.168.1.255'),
                FormParameter('nameServers', '8.8.8.8'),
                FormParameter('networkId', '')
            ]
        )

        response, ___ = self.request(
            As.admin, 'PUT', self.url,
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('broadcast', '192.168.1.255'),
                FormParameter('nameServers', '8.8.8.8,9.9.9.9,1.1.1.1'),
                FormParameter('networkId', '1.9.9.9'),
            ]
        )

        self.assertEqual(response['address'], '192.168.1.15')
        self.assertEqual(response['netmask'], '192.168.1.255')
        self.assertEqual(response['gateway'], '192.168.1.1')
        self.assertEqual(response['broadcast'], '192.168.1.255')
        self.assertEqual(response['nameServers'], '8.8.8.8 9.9.9.9 1.1.1.1')
        self.assertEqual(response['networkId'], '1.9.9.9')

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface('eth0')

        self.assertEqual(interface.address, '192.168.1.15')
        self.assertEqual(interface.netmask, '192.168.1.255')
        self.assertEqual(interface.gateway, '192.168.1.1')
        self.assertEqual(interface.broadcast, '192.168.1.255')
        self.assertEqual(interface.network, '1.9.9.9')
        self.assertEqual(interface['dns-nameservers'], '8.8.8.8 9.9.9.9 1.1.1.1')

        response, ___ = self.request(
            As.admin, 'PUT', self.url,
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('broadcast', '192.168.1.255'),
                FormParameter('nameServers', ''),
                FormParameter('networkId', '1.9.9.9'),
            ]
        )
        self.assertEqual(response['address'], '192.168.1.15')
        self.assertEqual(response['netmask'], '192.168.1.255')
        self.assertEqual(response['gateway'], '192.168.1.1')
        self.assertEqual(response['broadcast'], '192.168.1.255')
        self.assertEqual(response['nameServers'], '')
        self.assertEqual(response['networkId'], '1.9.9.9')

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface('eth0')

        self.assertEqual(interface.address, '192.168.1.15')
        self.assertEqual(interface.netmask, '192.168.1.255')
        self.assertEqual(interface.gateway, '192.168.1.1')
        self.assertEqual(interface.broadcast, '192.168.1.255')
        self.assertEqual(interface.network, '1.9.9.9')

        # Invalid address
        self.request(
            As.admin, 'PUT', self.url,
            params=[
                FormParameter('address', ''),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', '192.168.1.1'),
                FormParameter('broadcast', '192.168.1.255'),
                FormParameter('nameServers', ''),
                FormParameter('networkId', '1.9.9.9'),
            ],
            expected_status=400
        )

        # Update only require fields
        response, ___ = self.request(
            As.admin, 'PUT', self.url,
            params=[
                FormParameter('address', '192.168.1.15'),
                FormParameter('netmask', '192.168.1.255'),
                FormParameter('gateway', ''),
                FormParameter('broadcast', ''),
                FormParameter('nameServers', ''),
                FormParameter('networkId', ''),
            ]
        )

        self.assertEqual(response['address'], '192.168.1.15')
        self.assertEqual(response['netmask'], '192.168.1.255')
        self.assertEqual(response['gateway'], '')
        self.assertEqual(response['broadcast'], '')
        self.assertEqual(response['nameServers'], '')
        self.assertEqual(response['networkId'], '')

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface('eth0')

        self.assertEqual(interface.address, '192.168.1.15')
        self.assertEqual(interface.netmask, '192.168.1.255')

        self.logout()


if __name__ == '__main__':
    unittest.main()
