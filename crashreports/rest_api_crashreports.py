from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from rest_framework.permissions import AllowAny

from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


from rest_framework.permissions import BasePermission

from rest_framework.authtoken.models import Token

from crashreports.models import Crashreport
from crashreports.serializers import CrashReportSerializer

# class IsCreationAndHasCreationRights(BasePermission):
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated():
#             if view.action == 'create':
#                 if request.user.has_permission(""):
#                     return True
#                 return False
#         else:
#             return True
# 

class ListCreateCrashReport(generics.ListCreateAPIView):
    queryset = Crashreport.objects.all()
    paginate_by = 20
    permission_classes = (IsAuthenticated, )
    serializer_class = CrashReportSerializer
    pass
