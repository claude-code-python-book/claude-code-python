from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.CharField(max_length=20, unique=True)),
                ("customer", models.CharField(max_length=100)),
                ("gross", models.DecimalField(decimal_places=2, max_digits=12)),
                ("issued", models.DateField()),
                ("paid", models.DateField(blank=True, null=True)),
            ],
        ),
    ]
