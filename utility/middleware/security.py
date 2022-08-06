from django.utils.cache import add_never_cache_headers
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.contrib.sessions.models import Session


class DisableClientSideCachingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


class UserRestrictMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Checks if different session exists for user and deletes it.
        """
        if request.user.is_authenticated:
            cache_timeout = 86400
            cache_key = "user_pk_%s_restrict" % request.user.pk
            cache_value = cache.get(cache_key)

            if cache_value is not None:
                if request.session.session_key != cache_value:
                    session = Session(session_key=cache_value)
                    session.delete()
                    cache.set(cache_key, request.session.session_key,
                              cache_timeout)
            else:
                cache.set(cache_key, request.session.session_key, cache_timeout)
