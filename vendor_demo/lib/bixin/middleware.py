from django.utils.functional import SimpleLazyObject

from bixin.models import User


class FakeUser(object):
    id = 0
    username = ''

    def is_authenticated(self):
        return False

    def __unicode__(self):
        return 'Fake User'


def get_platform_user(request):
    if not hasattr(request, '_cached_platform_user'):
        user = None
        site_userid = request.session.get('site_userid')
        if site_userid:
            try:
                user = User.objects.get(id=site_userid)
                request._cached_platform_user = user
            except User.DoesNotExist:
                pass

        if user:
            request._cached_platform_user = user
        else:
            request._cached_platform_user = FakeUser()

    return request._cached_platform_user


class AuthenticationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'session')
        request.bx_user = SimpleLazyObject(
            lambda: get_platform_user(request))

        response = self.get_response(request)

        return response
