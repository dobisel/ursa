from nanohttp import RestController, json
from restfulpy.authorization import authorize

from ursa.system import get_system_manager


class SystemController(RestController):

    @json
    @authorize('admin')
    def reboot(self):
        system_manager = get_system_manager()
        system_manager.reboot()
        return system_manager.to_dict()

    @json
    @authorize('admin')
    def shutdown(self):
        system_manager = get_system_manager()
        system_manager.shutdown()
        return system_manager.to_dict()
