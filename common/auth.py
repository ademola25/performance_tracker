from django.conf import settings
from common.services.ad_auth import ADAuthentication
from django.contrib.auth.signals import (
    user_login_failed
)


class BasicAuthentication:
    @staticmethod
    def ad_auth_web(email, password, user, context):
        allow = False
        # Is AD Enabled
        is_ad_enabled = getattr(settings, "ENABLE_AD", False)
        ad_url = getattr(settings, "AD_URL", False)
        if is_ad_enabled and ad_url:
            ad_auth = ADAuthentication(ad_url)
            ad_response = ad_auth.authenticate(email, password)
            if ad_response:
                allow = True
                user.set_password(password)
                user.save()
            else:
                user_login_failed.send(sender=__name__,
                                       credentials={'username': email},
                                       request=context)
        else:
            allow = True
        return allow
