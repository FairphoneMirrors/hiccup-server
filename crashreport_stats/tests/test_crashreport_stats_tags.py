"""Tests for the crashreport stats template tags."""

from django.template import Context, Template
from django.test import TestCase

from crashreport_stats.tests.utils import Dummy


class CrashreportStatsTemplateTagsTests(TestCase):
    """Test rendering of the crashreport stats template tags."""

    @staticmethod
    def _create_template(template_name, parameter_keys):
        parameters_string = " ".join(
            ["{}={}".format(key, key) for key in parameter_keys]
        )

        load_template_tag_format = (
            "{{% load crashreport_stats_tags %}} {{% {} {} %}}"
        )
        template_load_string = load_template_tag_format.format(
            template_name, parameters_string
        )

        return Template(template_load_string)

    def _assert_rendered_template_contains(
        self, template_name, parameters, *expected_contents
    ):
        template = self._create_template(template_name, parameters.keys())

        rendered = template.render(Context(parameters))

        for expected_content in expected_contents:
            self.assertIn(expected_content, rendered)

    def test_device_overview_template(self):
        """Test rendering of the device overview template."""
        template_name = "device_overview"

        title = "Device Overview Test"
        parameters = {"title": title, "uuid": Dummy.UUIDs[0]}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            Dummy.UUIDs[0],
            '"UUID:"',
            '"Board Date:"',
            '"Last Active:"',
            '"HeartBeats sent:"',
            '"Prob. Crashes:"',
            '"Prob. Crashes per Day:"',
            '"SMPLs:"',
            '"SMPLs per Day:"',
        )

    def test_device_crashreport_table_template(self):
        """Test rendering of the crashreport table template."""
        template_name = "device_crashreport_table"

        title = "Device Crashreport Table Test"
        parameters = {"title": title, "uuid": Dummy.UUIDs[0]}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            Dummy.UUIDs[0],
            '"Build Fingerprint"',
            '"Date"',
            '"Likely Reboot Reason"',
            '"Logfiles"',
        )

    def test_device_update_history_template(self):
        """Test rendering of the device update history template."""
        template_name = "device_update_history"

        title = "Device Update History Test"
        parameters = {"title": title, "uuid": Dummy.UUIDs[0]}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            Dummy.UUIDs[0],
            '"device_update_statistic"',
            '"Version"',
            '"Update Date"',
            '"HB"',
            '"PC"',
            '"SMPLs"',
        )

    def test_device_report_history_template(self):
        """Test rendering of the device report history template."""
        template_name = "device_report_history"

        title = "Device Report History Test"
        parameters = {"title": title, "uuid": Dummy.UUIDs[0]}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            Dummy.UUIDs[0],
            "'Date'",
            "'Heartbeats'",
            "'prob. Crashes'",
            "'SMPL'",
            "'other'",
        )

    def test_versions_table_template(self):
        """Test rendering of the versions table template."""
        template_name = "versions_table"

        title = "FP2 OS Versions Test"
        parameters = {"title": title, "is_official_release": True}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            'is_official_release: "True"',
            '"versions_overview_table"',
            '"Version"',
            '"HB"',
            '"PC"',
            '"SMPLs"',
        )

    def test_versions_pie_chart_template(self):
        """Test rendering of the versions pie chart template."""
        template_name = "versions_pie_chart"

        title = "FP2 Version Distribution Test"
        parameters = {"title": title, "is_official_release": True}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            'is_official_release: "True"',
            '"versions_overview_pie_chart"',
        )

    def test_versions_area_chart_template(self):
        """Test rendering of the versions area chart template."""
        template_name = "versions_area_chart"

        title = "FP2 Version Distribution Test"
        parameters = {"title": title, "is_official_release": True}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            'is_official_release: "True"',
            '"versions_overview_area_chart"',
        )

    def test_versions_bar_chart_template(self):
        """Test rendering of the versions bar chart template."""
        template_name = "versions_bar_chart"

        title = "Version Stability Test"
        parameters = {"title": title, "is_official_release": True}

        self._assert_rendered_template_contains(
            template_name,
            parameters,
            title,
            'is_official_release: "True"',
            '"versions_overview_bar_chart"',
        )
