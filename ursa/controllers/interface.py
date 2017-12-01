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
    # @validate_form(whitelist=['title'])
    def put(self):
        pass
