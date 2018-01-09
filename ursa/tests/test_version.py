import unittest

from ursa.tests.helpers import WebTestCase, As


class VersionTestCase(WebTestCase):

    def test_version(self):
        response, ___ = self.request(As.anonymous, 'GET', '/apiv1/version')
        import ursa
        self.assertEqual(response['version'], ursa.__version__)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
