from nanohttp import RestController

from .interface import InterfacesController


class NetworkController(RestController):
    interfaces = InterfacesController()




