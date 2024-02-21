import argparse
import os

from django.core.management.base import BaseCommand, CommandError

from pol.import_export.resources import PolResource, BulkPolResource
from pol.import_export.adapters import Adapters


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("--filename", type=str, required=True)
        parser.add_argument(
            "--dry-run", default=False, action=argparse.BooleanOptionalAction
        )
        parser.add_argument(
            "--stop-on-error", default=True, action=argparse.BooleanOptionalAction
        )

    def handle(self, filename, dry_run, stop_on_error, *args, **options):
        Adapter = Adapters.get(os.path.splitext(filename)[1])
        if not Adapter:
            raise CommandError("Not supported file extension")
        if not os.path.exists(filename):
            raise CommandError("File not found")
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run, data won't be imported..."))
        else:
            self.stdout.write(self.style.SUCCESS("Starting import..."))
        adapter = Adapter(filename)
        bulk_import_resource = BulkPolResource()
        import_resource = PolResource()
        totals = {}
        for data in adapter.iter_chunks(stop_on_error):
            result = bulk_import_resource.import_data(data, dry_run=dry_run)
            for key, value in result.totals.items():
                totals[key] = totals.get(key, 0) + value
            self.stdout.ending = "\n"
            if result.has_errors():
                result = import_resource.import_data(data, dry_run=dry_run)
                for _, errors in result.row_errors():
                    for error in errors:
                        self.stdout.write(self.style.WARNING(f"{error.row}"))
                        self.stdout.write(self.style.ERROR(f"   {error.error}"))
                if stop_on_error:
                    return
            self.stdout.write(
                ", ".join(f"{k}: {v}" for k, v in totals.items()), ending="\r"
            )
        if not dry_run:
            self.stdout.write(", ".join(f"{k}: {v}" for k, v in totals.items()))
            self.stdout.write(
                self.style.SUCCESS(f"{filename} has been imported, {dry_run}")
            )
