from copy import deepcopy
from openwisp_controller.config.tests.utils import CreateDeviceGroupMixin
from openwisp_controller.geo.tests.utils import TestGeoMixin
from openwisp_users.tests.test_api import AuthenticationMixin
from openwisp_users.tests.utils import TestMultitenantAdminMixin

from openwisp_monitoring.device.tests.test_admin import DeviceData
from . import DeviceMonitoringTestCase, TestWifiClientSessionMixin

from swapper import load_model

Chart = load_model("monitoring", "Chart")
Metric = load_model("monitoring", "Metric")

class TestDeviceApiProbe(AuthenticationMixin, TestGeoMixin, DeviceMonitoringTestCase):
    """Tests if Inz probe data is accepted by api"""

    # Exclude general metrics from the query
    metric_queryset = Metric.objects.exclude(object_id=None)
    # Exclude general charts from the query
    chart_queryset = Chart.objects.exclude(metric__object_id=None)

    # TODO: move to mixin
    def _get_test_probe_data(self):
        return {
            "type": "DeviceMonitoring",
            "test_probe":{
                "test_field":"2137",
                "some_field": "test"
                }
            }

    def _create_device_data(self, **kwargs):
        d = self._create_device(**kwargs)
        return DeviceData(pk=d.pk)

    # def test_sanity_check(self):
    #     self.assertTrue(False)

    def test_api_200(self):
        o = self._create_org()
        d = self._create_device(organization=o)
        data = self._get_test_probe_data()
        with self.assertNumQueries(3):
            r = self._post_data(d.id, d.key, data)
        self.assertEqual(r.status_code, 200)
        # Add 1 for general metric and chart
        self.assertEqual(self.metric_queryset.count(), 0)
        self.assertEqual(self.chart_queryset.count(), 0)

        d.delete(check_deactivated=False)
        r = self._post_data(d.id, d.key, data)
        self.assertEqual(r.status_code, 404)

    def test_save_data(self):
        dd = self._create_device_data()
        dd.data = deepcopy(self._get_test_probe_data())
        dd.save_data()
        return dd

    def test_read_data(self):
        dd = self.test_save_data()
        dd = DeviceData(pk=dd.pk)
        self.assertEqual(dd.data, self._get_test_probe_data())