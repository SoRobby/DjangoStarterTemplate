# Generated by Django 4.2.4 on 2023-11-02 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0002_alter_country_options_alter_country_country_code_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="country_code",
            field=models.CharField(
                help_text="Code of the country (e.g., US, UK, etc...)",
                max_length=16,
                verbose_name="Country code",
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="Server date and time when the item was created modified",
                verbose_name="Date created",
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="date_modified",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Server date and time when the item was last modified",
                verbose_name="Date modified",
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="phone_code",
            field=models.IntegerField(
                help_text="Phone code of the country (e.g., 1, 44, etc...)",
                verbose_name="Phone code",
            ),
        ),
        migrations.AlterField(
            model_name="country",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                help_text="Unique identifier for the item",
                unique=True,
                verbose_name="UUID",
            ),
        ),
        migrations.CreateModel(
            name="UserCreatedAndModifiedModel",
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
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Unique identifier for the item",
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="Server date and time when the item was created modified",
                        verbose_name="Date created",
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Server date and time when the item was last modified",
                        verbose_name="Date modified",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="User who created the item",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_created_by_set",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        help_text="User who last modified the item",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(app_label)s_%(class)s_modified_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Modified by",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
