from datetime import datetime, timedelta
from django.test import TestCase
from django.core.cache import cache
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from swapper import load_model
from pytz import UTC

from openwisp_utils.tests import catch_signal

from openwisp_monitoring.device.tests import TestDeviceMonitoringMixin
from openwisp_monitoring.device.tests.test_admin import DeviceData

from .. import settings as app_settings
from ..exceptions import InvalidChartConfigException, InvalidMetricConfigException
from ..signals import post_metric_write, pre_metric_write, threshold_crossed
from . import TestMonitoringMixin

start_time = timezone.now()
ten_minutes_ago = start_time - timedelta(minutes=10)
Metric = load_model("monitoring", "Metric")
AlertSettings = load_model("monitoring", "AlertSettings")
Notification = load_model("openwisp_notifications", "Notification")

class TestProbeModel(TestMonitoringMixin, TestCase):
    def tearDown(self):
        cache.clear()
        super().tearDown()

    def test_custom_get_or_create(self):
        m, created = Metric._get_or_create(name="probes", configuration="probes")
        self.assertTrue(created)
        m2, created = Metric._get_or_create(name="probes", configuration="probes")
        self.assertEqual(m.id, m2.id)
        self.assertFalse(created)

    def test_batch_metric_write_no_data(self):
        m = self._create_general_metric(name="probes", configuration="probes")
        with self.assertNumQueries(0):
            Metric.batch_write(
                []
            )

    def test_batch_write_single_host(self):
        m = self._create_general_metric(
            # name="probes",
            configuration="probes",
            name = f"10.0.0.1 probes",
            main_tags={"ip": Metric._makekey("10.0.0.1")}
        )
        extra_values = {"mac":"12-34-45-67-89-0A", "device_timestamp": 1771427134, "flood_flag":0, "interface":"eth0" }
        Metric.batch_write(
            [
                (
                    m,
                    {
                        "value": 0.2137,
                        "extra_values": extra_values
                    }
                )
            ]
        )

    def test_batch_write_single_host(self):
        m = self._create_general_metric(
            # name="probes",
            configuration="probes",
            name = f"10.0.0.1 probes",
            main_tags={"ip": Metric._makekey("10.0.0.1")}
        )
        extra_values = {"mac":"12-34-45-67-89-0A", "device_timestamp": 1771427134, "flood_flag":0, "interface":"eth0" }
        Metric.batch_write(
            [
                (
                    m,
                    {
                        "value": 0.2137,
                        "extra_values": extra_values
                    }
                )
            ]
        )

class TestProbeDeviceData(TestDeviceMonitoringMixin, TestCase):
    def tearDown(self):
        cache.clear()
        super().tearDown()

    def _create_device_data(self, **kwargs):
        d = self._create_device(**kwargs)
        return DeviceData(pk=d.pk)

    def test_write_probe_data(self):
        dd = self._create_device_data()
        ct = ContentType.objects.get_for_model(load_model("config", "Device"))
        time = datetime.now().replace(tzinfo=UTC)

        probes_data = [
            {
                "ip" :"10.0.0.1" ,
                "mac":"12-34-45-67-89-0A",
                "flood_flag":0,
                "interface":"eth0",
                "probes":[
                    {
                        "rtt": 1.23,
                        "timestamp": 1771427134,
                    }
                ],
            },
        ]
        dd.writer.write_device_metrics = []
        dd.writer._write_probes(probes_data, dd.pk, ct, time=time)

        assert(len(dd.writer.write_device_metrics) == 1)
        assert(dd.writer.write_device_metrics[0][0].name == '10.0.0.1 probes')
        assert(dd.writer.write_device_metrics[0][1]['value'] == 1.23)
        read_extra = dd.writer.write_device_metrics[0][1]['extra_values']
        assert(read_extra['mac'] == "12-34-45-67-89-0A")
        assert(read_extra['flood_flag'] == 0)
        assert(read_extra['interface'] == 'eth0')

    def test_write_probe_no_data(self):
        dd = self._create_device_data()
        ct = ContentType.objects.get_for_model(load_model("config", "Device"))
        time = datetime.now().replace(tzinfo=UTC)

        probes_data = [
            {
                "ip" :"10.0.0.1" ,
                "mac":"12-34-45-67-89-0A",
                "flood_flag":0,
                "interface":"eth0",
                "probes":[
                ],
            },
        ]
        dd.writer.write_device_metrics = []
        dd.writer._write_probes(probes_data, dd.pk, ct, time=time)

        assert(len(dd.writer.write_device_metrics) == 1)
        assert(dd.writer.write_device_metrics[0][0].name == '10.0.0.1 probes')
        assert(dd.writer.write_device_metrics[0][1]['value'] == -1)
        read_extra = dd.writer.write_device_metrics[0][1]['extra_values']
        assert(read_extra['mac'] == "12-34-45-67-89-0A")
        assert(read_extra['flood_flag'] == 0)
        assert(read_extra['interface'] == 'eth0')

    def test_write_probe_data_multiple_hosts(self):
        dd = self._create_device_data()
        ct = ContentType.objects.get_for_model(load_model("config", "Device"))
        time = datetime.now().replace(tzinfo=UTC)

        probes_data = [
            {
                "ip" :"10.0.0.1" ,
                "mac":"12-34-45-67-89-0A",
                "flood_flag":0,
                "interface":"eth0",
                "probes":[
                    {
                        "rtt": 1.23,
                        "timestamp": 1771427134,
                    }
                ],
            },
            {
                "ip" :"10.0.0.2" ,
                "mac" : "12-34-45-67-89-0A",
                "flood_flag":0,
                "interface":"eth0",
                "probes" : [
                    {
                        "rtt": 1.23,
                        "timestamp": 1771427134,
                    }
                ]
            }
        ]
        dd.writer.write_device_metrics = []
        dd.writer._write_probes(probes_data, dd.pk, ct, time=time)
        assert(len(dd.writer.write_device_metrics) == 2)
        assert(dd.writer.write_device_metrics[0][0].name == '10.0.0.1 probes')
        assert(dd.writer.write_device_metrics[1][0].name == '10.0.0.2 probes')


    def test_write_probe_data_multiple_probes(self):
        dd = self._create_device_data()
        ct = ContentType.objects.get_for_model(load_model("config", "Device"))
        time = datetime.now().replace(tzinfo=UTC)

        probes_data = [
            {
                "ip" :"10.0.0.1" ,
                "mac":"12-34-45-67-89-0A",
                "flood_flag":0,
                "interface":"eth0",
                "probes":[
                    {
                        "rtt": 1,
                        "timestamp": 1771427134,
                    },
                    {
                        "rtt": 2,
                        "timestamp": 1771427144,
                    },
                    {
                        "rtt": 3,
                        "timestamp": 1771427154,
                    },
                    {
                        "rtt": 4,
                        "timestamp": 1771427164,
                    },
                    {
                        "rtt": 5,
                        "timestamp": 1771427174,
                    },
                    {
                        "rtt": 6,
                        "timestamp": 1771427184,
                    }

                ],
            },
        ]
        dd.writer.write_device_metrics = []
        dd.writer._write_probes(probes_data, dd.pk, ct, time=time)

        assert(len(dd.writer.write_device_metrics) == 1)
        assert(dd.writer.write_device_metrics[0][0].name == '10.0.0.1 probes')
        assert(dd.writer.write_device_metrics[0][1]['value'] == 3.5)
        read_extra = dd.writer.write_device_metrics[0][1]['extra_values']
        assert(read_extra["rtt_median"] == 4)