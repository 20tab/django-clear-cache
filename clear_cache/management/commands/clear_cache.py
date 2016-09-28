from django.conf import settings
from django.core.cache import caches, InvalidCacheBackendError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""
    help = 'Clears the cache with the provided alias.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            'cache_alias', nargs='?', default='default', type=str)

    def handle(self, *args, **kwargs):
        cache_alias = kwargs['cache_alias']
        try:
            assert settings.CACHES
            cache = caches[cache_alias]
            cache.clear()
            self.stdout.write(
                'Cache "{}" has been cleared!\n'.format(cache_alias))
        except AttributeError:
            raise CommandError('You have no cache configured!\n')
        except InvalidCacheBackendError:
            raise CommandError(
                'Cache "{}" does not exist!\n'.format(cache_alias))
