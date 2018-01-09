import os

from nanohttp import settings
from restfulpy.utils import construct_class_by_name


class SystemManager:

    # noinspection PyMethodMayBeStatic
    def reboot(self):
        os.system(settings.system_manager.reboot_command)

    # noinspection PyMethodMayBeStatic
    def shutdown(self):
        os.system(settings.system_manager.shutdown_command)

    # noinspection PyMethodMayBeStatic
    def to_dict(self):
        return {}


def get_system_manager():
    return construct_class_by_name(settings.system_manager.default)
