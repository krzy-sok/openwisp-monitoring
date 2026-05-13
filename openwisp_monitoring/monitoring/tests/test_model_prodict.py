from datetime import datetime, timedelta
from django.test import TestCase
from django.core.cache import cache
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from swapper import load_model

from openwisp_monitoring.device.tests import TestDeviceMonitoringMixin
from openwisp_monitoring.device.tests.test_admin import DeviceData
from openwisp_monitoring.device.antisniff_classifier_iterface import get_prediction

from . import TestMonitoringMixin

start_time = timezone.now()
ten_minutes_ago = start_time - timedelta(minutes=10)
Metric = load_model("monitoring", "Metric")
AlertSettings = load_model("monitoring", "AlertSettings")
Notification = load_model("openwisp_notifications", "Notification")

class TestPredictModel(TestMonitoringMixin, TestCase):
    def tearDown(self):
        cache.clear()
        super().tearDown()

    def test_custom_get_or_create(self):
        m, created = Metric._get_or_create(name="sniffer_proba", configuration="sniffer_proba")
        self.assertTrue(created)
        m2, created = Metric._get_or_create(name="sniffer_proba", configuration="sniffer_proba")
        self.assertEqual(m.id, m2.id)
        self.assertFalse(created)

class TestPredictDeviceData(TestDeviceMonitoringMixin, TestCase):
    # def test_write_predict_data():
    #     pass
    def _create_device_data(self, **kwargs):
        d = self._create_device(**kwargs)
        return DeviceData(pk=d.pk)

    def test_get_prediction_inaccessible(self):
        dd = self._create_device_data()
        res = get_prediction(dd.pk, "10.0.0.1", 0.5, 0.5, 1, 0.5)
        assert(res == -1.0)