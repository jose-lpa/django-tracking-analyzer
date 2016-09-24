import factory
from factory import fuzzy

from tracking_analyzer.models import Tracker


class UserFactory(factory.DjangoModelFactory):
    """
    Factory model for the Django ``User`` model.
    """
    first_name = 'Test'
    last_name = 'User'
    username = factory.Sequence(lambda n: 'user_{0}'.format(n))
    email = factory.Sequence(lambda n: 'user_{0}@maykinmedia.nl'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'testing')
    # test --pytest-args "--cov-report xml --cov tracking_analyzer tests/ --cov-config .coveragerc --junit-xml=junit.xml --color=yes --pylint --pylint-rcfile=pylint.rc"

    class Meta:
        model = 'auth.User'


class PostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: 'Post {0}'.format(n))
    slug = factory.Sequence(lambda n: 'post-{0}'.format(n))
    body = factory.Faker('text')

    class Meta:
        model = 'tests.Post'


class TrackerFactory(factory.django.DjangoModelFactory):
    content_object = factory.SubFactory(PostFactory)
    ip_address = factory.Faker('ipv4')
    ip_country = 'NL'
    ip_region = 'Noord-Holland'
    ip_city = 'Amsterdam'
    device_type = factory.fuzzy.FuzzyChoice(
        choices=(choice[0] for choice in Tracker.DEVICE_TYPE))
    device = 'Other'
    browser = 'Firefox'
    browser_version = '47'
    system = 'Windows'
    system_version = 'Millenium Edition'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'tracking_analyzer.Tracker'
