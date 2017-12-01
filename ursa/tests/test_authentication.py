import unittest

from restfulpy.principal import JwtPrincipal
from restfulpy.testing import FormParameter

from ursa.tests.helpers import WebTestCase, As
from ursa.models import Member


class AuthenticationTestCase(WebTestCase):

    def test_login(self):

        self.request(
            As.everyone, 'POST', '/apiv1/sessions',
            expected_status=400,
        )

        user_name = self.session.query(Member).first().user_name

        self.request(
            As.everyone, 'POST', '/apiv1/sessions',
            expected_status=400,
            params=[
                FormParameter('userName', user_name),
                FormParameter('password', 'invalidPassword')
            ]
        )

        result, meta = self.request(
            As.everyone, 'POST', '/apiv1/sessions',
            expected_status=400,
            params=[
                FormParameter('userName', 'invalidUserName'),
                FormParameter('password', 'invalidPassword')
            ]
        )

        self.assertDictContainsSubset(result, dict(
            message='Bad Request',
        ))

        # Login
        result, meta = self.request(
            As.everyone, 'POST', '/apiv1/sessions',
            params=[
                FormParameter('userName', 'admin'),
                FormParameter('password', '123456')
            ]
        )
        self.assertIn('token', result)
        principal = JwtPrincipal.load(result['token'])
        self.assertIn('sessionId', principal.payload)
        self.assertDictContainsSubset(principal.payload, {
            'userName': 'admin',
            'roles': ['admin'],
        })

        # Request a protected resource
        self.request(As.admin, 'GET', '/', headers={'Authorization': 'Bearer %s' % result['token']})

        # Request a protected resource without token
        self.request(As.admin, 'GET', '/', expected_status=401)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
