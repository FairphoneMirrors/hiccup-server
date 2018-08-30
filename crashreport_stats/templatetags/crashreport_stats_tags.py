"""Django template tags for crashreport statistics."""

from django.template import Library, loader


register = Library()


@register.simple_tag
def device_overview(
    title="General Information", uuid="e1c0cc95-ab8d-461a-a768-cb8d9d7adb04"
):
    """Render general device information."""
    template = loader.get_template(
        "crashreport_stats/tags/device_overview.html"
    )
    return template.render(
        {"uuid": uuid, "title": title, "element_name": "device_overview"}
    )


@register.simple_tag
def device_crashreport_table(
    title="Crashreports", uuid="e1c0cc95-ab8d-461a-a768-cb8d9d7adb04"
):
    """Render device crashreport table."""
    template = loader.get_template(
        "crashreport_stats/tags/device_crashreport_table.html"
    )
    return template.render(
        {
            "uuid": uuid,
            "title": title,
            "element_name": "device_crashreport_table",
        }
    )


@register.simple_tag
def device_update_history(
    title="Update History", uuid="e1c0cc95-ab8d-461a-a768-cb8d9d7adb04"
):
    """Render device update history."""
    template = loader.get_template(
        "crashreport_stats/tags/device_update_history.html"
    )
    return template.render(
        {
            "uuid": uuid,
            "title": title,
            "element_name": "device_update_statistic",
        }
    )


@register.simple_tag
def device_report_history(
    title="Report History", uuid="e1c0cc95-ab8d-461a-a768-cb8d9d7adb04"
):
    """Render device report history."""
    template = loader.get_template(
        "crashreport_stats/tags/device_report_history.html"
    )
    return template.render(
        {"uuid": uuid, "title": title, "element_name": "device_report_history"}
    )


@register.simple_tag
def versions_table(title="FP2 OS Versions", is_official_release="1"):
    """Render versions table."""
    template = loader.get_template("crashreport_stats/tags/versions_table.html")
    return template.render(
        {
            "title": title,
            "is_official_release": is_official_release,
            "element_name": "versions_overview_table",
        }
    )


@register.simple_tag
def versions_pie_chart(
    title="FP2 Version Distribution", is_official_release="1"
):
    """Render versions pie chart."""
    template = loader.get_template(
        "crashreport_stats/tags/versions_pie_chart.html"
    )
    return template.render(
        {
            "title": title,
            "is_official_release": is_official_release,
            "element_name": "versions_overview_pie_chart",
        }
    )


@register.simple_tag
def versions_area_chart(
    title="FP2 Version Distribution", is_official_release="1"
):
    """Render versions area chart."""
    template = loader.get_template(
        "crashreport_stats/tags/versions_area_chart.html"
    )
    return template.render(
        {
            "title": title,
            "is_official_release": is_official_release,
            "element_name": "versions_overview_area_chart",
        }
    )


@register.simple_tag
def versions_bar_chart(title="Version Stability", is_official_release="1"):
    """Render versions bar chart."""
    template = loader.get_template(
        "crashreport_stats/tags/versions_bar_chart.html"
    )
    return template.render(
        {
            "title": title,
            "is_official_release": is_official_release,
            "element_name": "versions_overview_bar_chart",
        }
    )
