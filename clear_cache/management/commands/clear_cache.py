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
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def handle(self, *args, **kwargs):
        cache_alias = kwargs['cache_alias']
        interactive = kwargs['interactive']
        if interactive:
            confirm = input("""You have requested to clear the cache "{}".
This will IRREVERSIBLY DESTROY all data currently contained in that cache.
Are you sure you want to do this?
    Type 'yes' to continue, or 'no' to cancel: """.format(cache_alias))
        else:
            confirm = 'yes'

        if confirm == 'yes':
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
