
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

    @json
    def metadata(self):
        return {
            "name": "Interface",
            "primaryKeys": [
            ],
            "fields": {
                "address": {
                    "name": "address",
                    "key": "address",
                    "type_": "str",
                    "default": None,
                    "optional": False,
                    "pattern": "\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b",
                    "maxLength": 16,
                    "minLength": 8,
                    "message": "Invalid Value",
                    "watermark": "Address",
                    "label": "Address",
                    "icon": None,
                    "example": "192.168.1.5",
                    "primaryKey": False,
                    "readonly": False,
                    "protected": False
                },
                "netmask": {
                    "name": "netmask",
                    "key": "netmask",
                    "type_": "str",
                    "default": None,
                    "optional": False,
                    "pattern": "\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b",
                    "maxLength": 16,
                    "minLength": 8,
                    "message": "Invalid Value",
                    "watermark": "NetMask",
                    "label": "NetMask",
                    "icon": None,
                    "example": "255.255.255.0",
                    "primaryKey": False,
                    "readonly": False,
                    "protected": False
                },
                "gateway": {
                    "name": "gateway",
                    "key": "gateway",
                    "type_": "str",
                    "default": None,
                    "optional": True,
                    "pattern": "\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b",
                    "maxLength": 16,
                    "minLength": 8,
                    "message": "Invalid Value",
                    "watermark": "Gateway",
                    "label": "Gateway",
                    "icon": None,
                    "example": "192.168.1.1",
                    "primaryKey": False,
                    "readonly": False,
                    "protected": False
                },
                "broadcast": {
                    "name": "broadcast",
                    "key": "broadcast",
                    "type_": "str",
                    "default": None,
                    "optional": True,
                    "pattern": "\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b",
                    "maxLength": 16,
                    "minLength": 8,
                    "message": "Invalid Value",
                    "watermark": "Broadcast",
                    "label": "Broadcast",
                    "icon": None,
                    "example": "192.168.1.255",
                    "primaryKey": False,
                    "readonly": False,
                    "protected": False
                },
                "network": {
                    "name": "network",
                    "key": "network",
                    "type_": "str",
                    "default": None,
                    "optional": True,
                    "pattern": "\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b",
                    "maxLength": 16,
                    "minLength": 8,
                    "message": "Invalid Value",
                    "watermark": "Network",
                    "label": "Network",
                    "icon": None,
                    "example": "192.168.1.0",
                    "primaryKey": False,
                    "readonly": False,
                    "protected": False
                },
                "nameServers": {
                    "name": "nameServers",
                    "key": "nameServers",
                    "type_": "str",
                    "default": None,
                    "optional": True,
                    "pattern": None,
                    "maxLength": 16,
                    "minLength": 8,
                    "message": "Invalid Value",
                    "watermark": "NameServers",
                    "label": "NameServers",
                    "icon": None,
                    "example": "8.8.8.8 9.9.9.9",
                    "primaryKey": False,
                    "readonly": False,
                    "protected": False
                },
            }
        }
