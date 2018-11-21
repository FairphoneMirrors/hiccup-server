"""Views for the Hiccup statistics."""
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import user_passes_test
from django import forms
from django.contrib import messages
from django.urls import reverse

from crashreport_stats.permissions import check_user_is_hiccup_staff
from crashreports.models import Device


class DeviceUUIDForm(forms.Form):
    """Form for searching devices by UUID."""

    uuid = forms.CharField(label="Device UUID:", max_length=100)


@user_passes_test(check_user_is_hiccup_staff)
def device_stats(request):
    """Respond with statistics for a specific device."""
    template = loader.get_template("crashreport_stats/device.html")
    uuid = request.GET.get("uuid", "NO_UUID")
    if not Device.objects.filter(uuid=uuid).exists():
        raise Http404("Device doesn't exist.")
    return HttpResponse(template.render({"uuid": uuid}, request))


@user_passes_test(check_user_is_hiccup_staff)
def versions_all_overview(request):
    """Respond with the distribution of official release versions."""
    template = loader.get_template("crashreport_stats/versions.html")
    return HttpResponse(template.render({"is_official_release": "1"}, request))


@user_passes_test(check_user_is_hiccup_staff)
def versions_overview(request):
    """Respond with the distribution of non-official release versions."""
    template = loader.get_template("crashreport_stats/versions.html")
    return HttpResponse(template.render({"is_official_release": "2"}, request))


@user_passes_test(check_user_is_hiccup_staff)
def home(request):
    """Respond with a form for searching devices by UUID.

    When using a HTTP GET method, the search device form view is returned.
    The response additionally includes possible results if a HTTP POST message
    was sent. If a single device was found, a redirect to the device
    statistics of that device is sent.
    """
    devices = None
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = DeviceUUIDForm(request.POST)
        if form.is_valid():
            uuid = form.cleaned_data["uuid"]
            if not Device.objects.filter(uuid=uuid).exists():
                devices = Device.objects.filter(uuid__startswith=uuid)
                if len(devices) == 1:
                    return HttpResponseRedirect(
                        reverse("hiccup_stats_device")
                        + "?uuid="
                        + devices[0].uuid
                    )
                if not devices:
                    messages.warning(request, "No devices found.")
            else:
                return HttpResponseRedirect(
                    reverse("hiccup_stats_device") + "?uuid=" + uuid
                )
    else:
        form = DeviceUUIDForm()
    template = loader.get_template("crashreport_stats/home.html")
    return HttpResponse(
        template.render({"form": form, "devices": devices}, request)
    )
