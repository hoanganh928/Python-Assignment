from rest_framework.throttling import AnonRateThrottle


# Rate limit class: restricted by IP and company_id
class CustomThrottler(AnonRateThrottle):
    cache_format = 'throttle_%(scope)s_%(ident)s%(company_id)s'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None  # Only throttle unauthenticated requests.
        company_id = view.kwargs.get('company_id')
        cache_key = self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
            'company_id': company_id
        }
        return cache_key
