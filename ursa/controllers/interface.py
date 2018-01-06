
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
            interface_file.write('  broadcast 192.168.1.255\n')
            interface_file.write('  netmask 255.255.255.0\n')
            interface_file.write('  network 192.168.1.0\n')
            interface_file.write('  dns-nameservers 192.168.1.1\n')
            interface_file.close()

        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface(settings.network.default_interface)
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
        iface = InterfacesFile(settings.network.interfaces_file)
        interface = iface.get_iface(settings.network.default_interface)
        name_servers = context.form.get('nameServers')

        if ' ' in name_servers:
            seprator = ' '
        elif ',' in name_servers:
            seprator = ','
        elif ';' in name_servers:
            seprator = ';'
        elif '-' in name_servers:
            seprator = '-'
        else:
            seprator = None

        if seprator is not None:
            name_servers = ' '.join(name_servers.split(seprator))
        else:
            if name_servers == '' or name_servers is None:
                name_servers = context.form.get('gateway')

        for attr in ['dns-nameservers', 'address', 'netmask', 'gateway', 'broadcast', 'network']:
            if hasattr(interface, attr):
                setattr(interface, attr, '')

        interface['dns-nameservers'] = name_servers
        interface.address = context.form.get('address')
        interface.netmask = context.form.get('netmask')
        interface.gateway = context.form.get('gateway')
        interface.broadcast = context.form.get('broadcast')
        if name_servers is not None:
            interface.network = context.form.get('networkId')
        iface.save(validate=False)
        context.form['nameServers'] = name_servers
        return context.form
