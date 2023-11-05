# Generated by Django 4.2.4 on 2023-11-05 06:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0004_alter_subscriptionterm_interval"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionplan",
            name="features_json_list",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Features JSON list",
                null=True,
                verbose_name="Features JSON list",
            ),
        ),
    ]
