from nanohttp import RestController, json, context, settings, action
from restfulpy.authorization import authorize
from restfulpy.validation import validate_form
from network_interfaces import InterfacesFile


class InterfacesController(RestController):

    @json
    @authorize('admin')
    def get(self):
        pass

    @action
    @authorize('admin')
    @validate_form(whitelist=['address', 'netmask', 'gateway', 'DNS1', 'DNS2', 'network'])
    def put(self):
        iface = InterfacesFile(settings.interfaces_file_path)
        interface = iface.get_iface(settings.default_iface_title)
        interface.address = context.form.get('address')
        interface.netmask = context.form.get('netmask')
        interface.gateway = context.form.get('gateway')
        interface.DNS1 = context.form.get('DNS1')
        interface.DNS2 = context.form.get('DNS2')
        interface.network = context.form.get('network')
        iface.save(validate=False)

