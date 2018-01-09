
import os
from os import path

from nanohttp import RestController, json, context, settings, HttpBadRequest, HttpConflict
from restfulpy.authorization import authorize
from restfulpy.validation import validate_form
from network_interfaces import InterfacesFile


class InterfacesController(RestController):

    @classmethod
    def ensure_interfaces(cls):
        os.makedirs(path.dirname(settings.network.interfaces_file), exist_ok=True)
        if not path.exists(settings.network.interfaces_file):
            with open(settings.network.interfaces_file, 'w') as interface_file:
                interface_file.writelines([
                    f'iface {settings.network.default_interface} inet static\n',
                    '  address 192.168.1.12\n',
                    '  gateway 192.168.1.1\n',
                    '  broadcast 192.168.1.255\n',
                    '  netmask 255.255.255.0\n',
                    '  network 192.168.1.0\n',
                    '  dns-nameservers 192.168.1.1\n',
                ])

        return InterfacesFile(settings.network.interfaces_file)

    def ensure_default_interface(self, interfaces=None):
        interfaces = interfaces or self.ensure_interfaces()
        try:
            return interfaces.get_iface(settings.network.default_interface)
        except KeyError:
            raise HttpConflict(f'interface {settings.network.default_interface} not found.')

    @json
    @authorize('admin')
    def get(self):
        interface = self.ensure_default_interface()

        response = dict()
        response['address'] = getattr(interface, 'address', None)
        response['netmask'] = getattr(interface, 'netmask', None)
        response['gateway'] = getattr(interface, 'gateway', None)
        response['broadcast'] = getattr(interface, 'broadcast', None)
        response['networkId'] = getattr(interface, 'network', None)
        response['nameServers'] = getattr(interface, 'dns-nameservers', None)
        return response

    @json
    @authorize('admin')
    @validate_form(exact=['address', 'netmask', 'gateway', 'broadcast', 'nameServers', 'networkId'])
    def put(self):
        if context.form.get('address') is None or context.form.get('address') == '' or\
                context.form.get('netmask') is None or context.form.get('netmask') == '':
            raise HttpBadRequest()

        interfaces = self.ensure_interfaces()
        interface = self.ensure_default_interface(interfaces)

        for attr in ['dns-nameservers', 'address', 'netmask', 'gateway', 'broadcast', 'network']:
            if hasattr(interface, attr):
                setattr(interface, attr, '')

        name_servers = context.form.get('nameServers')

        if name_servers is not None:
            if ' ' in name_servers:
                separator = ' '
            elif ',' in name_servers:
                separator = ','
            elif ';' in name_servers:
                separator = ';'
            elif '-' in name_servers:
                separator = '-'
            else:
                separator = None

            if separator is not None:
                name_servers = ' '.join(name_servers.split(separator))

            interface['dns-nameservers'] = name_servers

        interface.address = context.form.get('address')
        interface.netmask = context.form.get('netmask')

        if context.form.get('gateway') is not None:
            interface.gateway = context.form.get('gateway')

        if context.form.get('broadcast') is not None:
            interface.broadcast = context.form.get('broadcast')

        if context.form.get('networkId') is not None:
            interface.network = context.form.get('networkId')

        interfaces.save(validate=False)
        context.form['nameServers'] = name_servers
        return context.form
