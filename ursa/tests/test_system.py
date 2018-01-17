import unittest

from nanohttp import settings

from ursa.tests.helpers import WebTestCase, As

is_rebooted = False
is_shutted_down = False


class MockupSystemManager:

    # noinspection PyMethodMayBeStatic
    def reboot(self):
        global is_rebooted
        is_rebooted = True

    # noinspection PyMethodMayBeStatic
    def shutdown(self):
        global is_shutted_down
        is_shutted_down = True

    # noinspection PyMethodMayBeStatic
    def to_dict(self):
        return {}


class SystemTestCase(WebTestCase):
    url = '/apiv1/system'

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge("""
            system_manager: 
              default: ursa.tests.test_system.MockupSystemManager
        """)

    def test_reboot(self):
        self.logout()
        self.request(As.anonymous, 'REBOOT', self.url, expected_status=401)

        self.login_as_admin()
        global is_rebooted
        is_rebooted = False
        self.request(As.admin, 'REBOOT', self.url)
        self.assertTrue(is_rebooted)

    def test_shutdown(self):
        self.logout()
        self.request(As.admin, 'SHUTDOWN', self.url, expected_status=401)

        self.login_as_admin()
        global is_shutted_down
        is_shutted_down = False
        self.request(As.admin, 'SHUTDOWN', self.url)
        self.assertTrue(is_shutted_down)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
