from nanohttp import RestController, json, context, HttpBadRequest
from restfulpy.logging_ import get_logger


logger = get_logger('auth')


class SessionsController(RestController):

    @json
    def post(self):
        user_name = context.form.get('userName')
        password = context.form.get('password')

        def bad():
            logger.info('Login failed: %s' % user_name)
            raise HttpBadRequest('Invalid username or password')

        if not (user_name and password):
            bad()

        logger.info('Trying to login: %s' % user_name)
        principal = context.application.__authenticator__.login((user_name, password))
        if principal is None:
            bad()

        return dict(token=principal.dump())
