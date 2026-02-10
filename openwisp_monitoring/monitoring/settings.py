from ..settings import get_settings_value
from django.utils.translation import gettext_lazy as _

from openwisp_monitoring.db import chart_query

ADDITIONAL_CHARTS = get_settings_value("CHARTS", {})
ADDITIONAL_METRICS = get_settings_value("METRICS",
    {
        "test_probe": {
            "label": "test_probe",
            "name": "test_probe",
            "key": "test_field",
            "field_name": "test_field",
            "related_fields": ["some_field"],
            "charts": {
                "test_probe_chart": {
                    "type": "bar",
                    "title": _("Sample chart"),
                    "description": _(
                        "test probe chart"
                    ),
                    "summary_labels": [_("Sample chart")],
                    "unit": "num",
                    "order": 200,
                    "query": {
                        "influxdb":("SELECT test_field from test_field")
                    }
                }
            }
        },
        "probes": {
            "label": "probes",
            "name": "probes",
            "key": "ip",
            "field_name": "ip",
            # all fields are keys in influx - meaning indexed and can group by them
            "related_fields": ["mac" , "rtt", "device_timestamp"],
            "charts": {
                "probe_rtt_chart": {
                    "type": "bar",
                    "title": _("Probe rtt chart"),
                    "description": _(
                        "example chart"
                    ),
                    "summary_labels": [_("Sample chart")],
                    "unit": "num",
                    "order": 200,
                    "query": {
                        "influxdb":("SELECT rtt from test_field")
                    }
                }
            }
        }
    }
)

RETRY_OPTIONS = get_settings_value(
    "WRITE_RETRY_OPTIONS",
    dict(
        max_retries=None, retry_backoff=True, retry_backoff_max=600, retry_jitter=True
    ),
)
ADDITIONAL_DASHBOARD_TRAFFIC_CHART = get_settings_value("DASHBOARD_TRAFFIC_CHART", {})
TOLERANCE_INTERVAL = get_settings_value("TOLERANCE_INTERVAL", 300)
