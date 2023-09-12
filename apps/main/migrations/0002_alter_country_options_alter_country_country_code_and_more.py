# Generated by Django 4.2.4 on 2023-09-11 06:12

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="country",
            options={"ordering": ("name",), "verbose_name_plural": "Countries"},
        ),
        migrations.AlterField(
            model_name="country",
            name="country_code",
            field=models.CharField(
                help_text="Code of the country (e.g., US, UK, etc.)", max_length=16
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="phone_code",
            field=models.IntegerField(
                help_text="Phone code of the country (e.g., 1, 44, etc.)",
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="slug",
            field=models.SlugField(
                default=django.utils.timezone.now,
                help_text="The slug based on the country name",
                max_length=255,
                unique=True,
            ),
            preserve_default=False,
        ),
    ]