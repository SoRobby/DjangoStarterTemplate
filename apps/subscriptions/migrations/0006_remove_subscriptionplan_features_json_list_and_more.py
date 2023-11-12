# Generated by Django 4.2.4 on 2023-11-05 07:12

import apps.subscriptions.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0005_subscriptionplan_features_json_list"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscriptionplan",
            name="features_json_list",
        ),
        migrations.AddField(
            model_name="subscriptionplan",
            name="features_list",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text='Features JSON list, features are separated by comma (e.g.,                                          ["5 products", "Basic analytics", ...])',
                null=True,
                validators=[apps.subscriptions.models.validate_features_list],
                verbose_name="Features JSON list",
            ),
        ),
    ]
