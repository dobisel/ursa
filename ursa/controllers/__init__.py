
from nanohttp import html, json, RestController
import ursa


class ApiV1(RestController):

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
