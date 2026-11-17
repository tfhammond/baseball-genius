import argparse
import os

import django
from django.db import connection, transaction


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name starting with setup-demo-")
    parser.add_argument("--read-only", action="store_true")
    args = parser.parse_args()
    if not args.name.startswith("setup-demo-") or len(args.name) > 150:
        parser.error("Use a name starting with setup-demo- (max 150 characters)")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    from django.contrib.auth.models import Group

    if not args.read_only:
        with transaction.atomic():
            row, created = Group.objects.get_or_create(name=args.name)
        status = "Inserted" if created else "Already stored"
        print(f"{status}: id={row.pk}, name={row.name}")
        connection.close()

    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database()")
        database_name = cursor.fetchone()[0]

    row = Group.objects.filter(name=args.name).first()
    if row is None:
        parser.exit(1, f"Row not found in {database_name}: {args.name}\n")
    print(f"PostgreSQL: {connection.settings_dict['HOST']} / {database_name}")
    print(f"Read back: id={row.pk}, name={row.name}")


if __name__ == "__main__":
    main()
