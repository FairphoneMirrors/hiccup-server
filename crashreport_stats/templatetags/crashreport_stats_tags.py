from django import template
from django.template import loader

register = template.Library()

@register.simple_tag
def device_overview(title = "General Information", uuid='e1c0cc95-ab8d-461a-a768-cb8d9d7adb04'):
    t = template.loader.get_template('crashreport_stats/tags/device_overview.html')
    return t.render({
        'uuid': uuid,
        "title": title,
        "element_name": "device_overview"})

@register.simple_tag
def device_crashreport_table(title = "Crashreports", uuid='e1c0cc95-ab8d-461a-a768-cb8d9d7adb04'):
    t = template.loader.get_template('crashreport_stats/tags/device_crashreport_table.html')
    return t.render({
        'uuid': uuid,
        "title": title,
        "element_name": "device_crashreport_table"})

@register.simple_tag
def device_update_history(title = "Update History", uuid='e1c0cc95-ab8d-461a-a768-cb8d9d7adb04'):
    t = template.loader.get_template('crashreport_stats/tags/device_update_history.html')
    return t.render({
        'uuid': uuid,
        "title": title,
        "element_name": "device_update_statistic"})

@register.simple_tag
def device_report_history(title = "Report History", uuid='e1c0cc95-ab8d-461a-a768-cb8d9d7adb04'):
    t = template.loader.get_template('crashreport_stats/tags/device_report_history.html')
    return t.render({
        'uuid': uuid,
        "title": title,
        "element_name": "device_report_history"})
