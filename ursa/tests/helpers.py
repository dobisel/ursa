
from restfulpy.testing import ModelRestCrudTestCase

import ursa
from ursa.models import Admin


class WebTestCase(ModelRestCrudTestCase):
    application = ursa.ursa

    def login(self, user_name, password):
        result, metadata = self.request(None, 'POST', '/apiv1/sessions', doc=False, params={
            'userName': user_name,
            'password': password
        })
        self.wsgi_app.jwt_token = result['token']
        return user_name, password

    def logout(self):
        self.wsgi_app.jwt_token = ''

    @classmethod
    def mockup(cls):

        admin = Admin()
        admin.password = '123456'
        admin.user_name = 'admin'
        cls.session.add(admin)

        cls.session.commit()

    def login_as_admin(self):
        return self.login('admin', '123456')


class As:
    anonymous = 'Visitor'
    admin = 'Admin'
    everyone = '|'.join((admin, anonymous))
