
import os.path

from nanohttp import RestController, json, context, settings, HttpBadRequest
from restfulpy.authorization import authorize
from restfulpy.validation import validate_form
from network_interfaces import InterfacesFile


class InterfacesController(RestController):

    @json
    @authorize('admin')
    def get(self):

        if not os.path.isfile(settings.network.interfaces_file):
            if not os.path.isdir(settings.network.interfaces_dir):
                os.makedirs(settings.network.interfaces_dir)

            interface_file = open(settings.network.interfaces_file, 'w')
            interface_file.write(f'iface {settings.network.default_interface} inet static\n')
            interface_file.write('  address 192.168.1.12\n')
            interface_file.write('  gateway 192.168.1.1\n')
            interface_file.write('  netmask 255.255.255.0\n')
            interface_file.write('  network 192.168.1.0\n')
            interface_file.write('  nameservers 192.168.1.1\n')
            interface_file.close()

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface(settings.network.default_interface)
        response = dict()
        response['address'] = interface.address
        response['netmask'] = interface.netmask
        response['gateway'] = interface.gateway
        response['networkId'] = interface.network
        response['nameServers'] = interface.nameservers
        return response

    @json
    @authorize('admin')
    @validate_form(exact=['address', 'netmask', 'gateway', 'nameServers', 'networkId'])
    def put(self):
        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface(settings.network.default_interface)
        name_servers = context.form.get('nameServers')
        if len(name_servers.split(' ')) > 2:
            raise HttpBadRequest()
        interface.nameservers = context.form.get('nameServers')
        interface.address = context.form.get('address')
        interface.netmask = context.form.get('netmask')
        interface.gateway = context.form.get('gateway')
        if name_servers is not None:
            interface.network = context.form.get('networkId')
        iface.save(validate=False)
        return context.form
