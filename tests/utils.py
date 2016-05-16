from django.contrib.auth.models import User
from django.test import RequestFactory
from django.utils.functional import SimpleLazyObject

from django_user_agents.utils import get_user_agent


def build_mock_request(url):
    """
    Helper function to manually build a ``WSGIRequest`` object to be used
    to test the view.

    :param url: A string representing the URL for the request.
    :return: A prepared ``WSGIRequest`` object.
    """
    # Build an interesting request.
    request = RequestFactory().get(url)
    request.COOKIES = {
        # Some silly cookies, just a PoC.
        'company': 'MaykinMedia',
        'worker': 'Jose',
    }
    request.META['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Macintosh; Intel Mac ' \
                                      'OS X 10_10_5) AppleWebKit/537.36 ' \
                                      '(KHTML, like Gecko) ' \
                                      'Chrome/49.0.2623.112 Safari/537.36'
    # Set up a known IP address to retrieve GeoIP data. This one is from
    # OpenDNS service, check https://www.opendns.com/
    request.META['REMOTE_ADDR'] = '208.67.222.222'

    # Request is performed by a system user.
    request.user, created = User.objects.get_or_create(
        username='test_user',
        first_name='Test',
        last_name='User',
        email='test_user@maykinmedia.nl'
    )

    # Set up the 'django-user-agent' machinery in the request, as its own
    # middleware does.
    request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))

    return request
