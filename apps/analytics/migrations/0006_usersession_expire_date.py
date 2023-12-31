# Generated by Django 4.2.4 on 2023-10-24 00:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("analytics", "0005_alter_usersession_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersession",
            name="expire_date",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time when the session expires",
                null=True,
            ),
        ),
    ]
