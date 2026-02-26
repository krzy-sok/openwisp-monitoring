from ..settings import get_settings_value
from django.utils.translation import gettext_lazy as _

from openwisp_monitoring.db import chart_query

ADDITIONAL_CHARTS = get_settings_value("CHARTS", {})
ADDITIONAL_METRICS = get_settings_value("METRICS",
    {
        "probes": {
            "label": "probes",
            "name": "probes",
            # key == table name
            "key": "probes",
            "field_name": "rtt_avg",
            "related_fields": ["mac", "device_timestamp", "flood_flag", "interface", "rtt_median", "individual_probes"],
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
