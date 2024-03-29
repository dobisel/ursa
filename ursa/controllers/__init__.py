
from nanohttp import html, json, RestController
from restfulpy.authorization import authorize
from restfulpy.controllers import RootController

import ursa
from ursa.controllers.system import SystemController
from ursa.controllers.network import NetworkController
from ursa.controllers.sessions import SessionsController


class ApiV1(RestController):
    network = NetworkController()
    system = SystemController()
    sessions = SessionsController()

    @json
    def version(self):
        return {
            'version': ursa.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

    @html
    @authorize
    def index(self):
        return 'Index'
