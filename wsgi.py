import os

from ursa import ursa

ursa.configure()
ursa.initialize_models()


def cross_origin_helper_app(environ, start_response):

    def better_start_response(status, headers):
        headers.append(('Access-Control-Allow-Origin', os.environ.get('TRUSTED_HOSTS', '*')))
        headers.append(('Access-Control-Allow-Credentials', 'true'))
        headers.append(('Access-Control-Allow-Headers', 'Content-Type, Authorization'))
        headers.append(('Access-Control-Expose-Headers', 'X-Pagination-Count'))
        headers.append(('Access-Control-Allow-Methods', 'PUT, REBOOT'))
        start_response(status, headers)

    return ursa(environ, better_start_response)


app = cross_origin_helper_app
