"""Utility functions for the crashreports app."""

from django.shortcuts import get_object_or_404


def get_object_by_lookup_fields(view, lookup_fields):
    """Retrieve an object using the provided lookup fields.

    Filter objects by the request parameters given in the view. Use only the
    parameters that are given in the lookup field keys set. If a single
    object instance matches the filters, it is returned. Otherwise a HTTP 404
    exception is raised.

    :param view: The view containing the request parameters.
    :param lookup_fields: Set of keys of request parameters to use.
    :return: The matched object.
    """
    queryset = view.get_queryset()
    query_filter = {}
    for field in lookup_fields:
        if field in view.kwargs:
            query_filter[field] = view.kwargs[field]
    obj = get_object_or_404(queryset, **query_filter)
    view.check_object_permissions(view.request, obj)
    return obj
