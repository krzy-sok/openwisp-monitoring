from openwisp_monitoring.check.admin import CheckAdmin  # noqa

CheckAdmin.list_display.insert(1, "my_custom_field")
