from openwisp_controller.config.tests.utils import CreateDeviceGroupMixin
from openwisp_controller.geo.tests.utils import TestGeoMixin
from openwisp_users.tests.test_api import AuthenticationMixin
from openwisp_users.tests.utils import TestMultitenantAdminMixin
from . import DeviceMonitoringTestCase, TestWifiClientSessionMixin

class TestDeviceApiProbe(AuthenticationMixin, TestGeoMixin, DeviceMonitoringTestCase):
    """Tests if Inz probe data is accepted by api"""

    # TODO: move to mixin
    def _get_test_probe_data():
        return {
            "type": "DeviceMonitoring",
            "test_probe":{
                "test_field":"2137",
                "some_field": "test"
                }
            }

    def test_are_test_loaded(self):
        self.assertTrue(True)

    def test_sanity_check(self):
        self.assertTrue(False)