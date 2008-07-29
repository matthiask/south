from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import models
from optparse import make_option
from south import migration
import sys

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--skip', action='store_true', dest='skip', default=False,
            help='Will skip over out-of-order missing migrations'),
        make_option('--merge', action='store_true', dest='merge', default=False,
            help='Will run out-of-order missing migrations as they are - no rollbacks.'),
        make_option('--only', action='store_true', dest='only', default=False,
            help='Only runs or rolls back the migration specified, and none around it.'),
    )
    help = "Runs migrations for all apps."

    def handle(self, target=None, skip=False, merge=False, only=False, backwards=False, **options):
        # Work out what the resolve mode is
        resolve_mode = merge and "merge" or (skip and "skip" or None)
        # Turn on db debugging
        from south.db import db
        db.debug = True
        # Migrate each app
        for app in models.get_apps():
            migrations = migration.get_migrations(app)
            if migrations is not None:
                migration.migrate_app(
                    migrations,
                    resolve_mode = resolve_mode,
                    target_name = target,
                )
                continue
