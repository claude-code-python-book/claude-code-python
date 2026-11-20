"""Enable btree_gist before any model needs it.

The no_double_booking exclusion constraint compares the room with =, which
GiST indexes support only through PostgreSQL's btree_gist extension.
"""

from django.contrib.postgres.operations import BtreeGistExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = []

    operations = [BtreeGistExtension()]
