from models import PSensorSetting
from rest_framework import viewsets
from serializers import PSensorSettingSerializer
from rest_framework.permissions import BasePermission

class IsCreationOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True


class PSensorSettingViewSet(viewsets.ModelViewSet):
    queryset = PSensorSetting.objects.all()
    serializer_class =  PSensorSettingSerializer
    permission_classes = [IsCreationOrIsAuthenticated]
