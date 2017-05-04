from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

class FairphoneAccountAdapter(DefaultSocialAccountAdapter):
    
    def is_open_for_signup(self, request, sociallogin):
        return True
    
    def save_user(self, request, sociallogin, form=None):
        u =DefaultSocialAccountAdapter.save_user(self, request, sociallogin, form=None)
        if u.email.split('@')[1] == "fairphone.com":
            g = Group.objects.get(name='FairphoneSoftwareTeam') 
            g.user_set.add(u)
        return u
            
    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        u = DefaultSocialAccountAdapter.populate_user(self,request,sociallogin,data)
        if not u.email.split('@')[1] == "fairphone.com":
             raise PermissionDenied()
        return u

class FormAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False
