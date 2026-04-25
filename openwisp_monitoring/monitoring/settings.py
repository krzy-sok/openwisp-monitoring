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
                "probe_avg_chart": {
                    "type": "bar",
                    "title": _("Probe avg rtt chart for {ip}"),
                    "description": _(
                        "average rtt of probes sent to host {ip}"
                    ),
                    "summary_labels": [_("Sample chart")],
                    "unit": "",
                    "order": 200,
                    "query": {
                        "influxdb":("SELECT rtt_avg FROM probes WHERE ip = '{ip}' and time >= '{time}' and object_id = '{object_id}'")
                    }
                },
                "probe_med_chart": {
                    "type": "bar",
                    "title": _("Probe median rtt chart for {ip}"),
                    "description": _(
                        "median rtt of probes sent to host {ip}"
                    ),
                    "summary_labels": [_("Sample chart")],
                    "unit": "",
                    "order": 200,
                    "query": {
                        "influxdb":("SELECT rtt_median FROM probes WHERE ip = '{ip}' and time >= '{time}' and object_id = '{object_id}'")
                    }
                }
            }
        },
        "sniffer_proba": {
            "label": "sniffer_proba",
            "name": "sniffer_proba",
            # key == table name
            "key": "sniffer_proba",
            "field_name": "probability",
            "related_fields": [],
            "charts": {
                "sniffer_chart": {
                    "type": "line",
                    "title": _("Sniffer probability chart for {ip}"),
                    "description": _(
                        "Probability of sniffer running on a host {ip}"
                    ),
                    "summary_labels": [_("Sample chart")],
                    "unit": "",
                    "order": 200,
                    "query": {
                        "influxdb":("SELECT probability FROM sniffer_proba WHERE ip = '{ip}' and time >= '{time}' and object_id = '{object_id}'")
                    }
                }
            },
            "notification":{
                "problem": {
                    "verbose_name": "Anti-sniffer PROBLEM",
                    "verb": _("host {ip} is likely to be running a sniffer"),
                    "level": "warning",
                    "email_subject": _(
                        "[{site.name}] PROBLEM: {notification.target} {notification.verb}"
                    ),
                    "message": _(
                        "The device [{notification.target}]({notification.target_link}) "
                        "{notification.verb}."
                    ),
                },
                "recovery": {
                    "verbose_name": "Anti-sniffer RECOVERY",
                    "verb": _("host {ip} has returned to normal sniffer risk"),
                    "level": "info",
                    "email_subject": _(
                        "[{site.name}] RECOVERY: {notification.target} {notification.verb}"
                    ),
                    "message": _(
                        "The device [{notification.target}]({notification.target_link}) "
                        "{notification.verb}."
                    ),
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
