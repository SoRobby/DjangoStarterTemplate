# Generated by Django 4.2.4 on 2023-11-06 03:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0008_subscriptionplan_plan_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscriptionplan",
            name="plan_category",
            field=models.CharField(
                choices=[("default", "Default")],
                default="default",
                help_text="Allows for multiple subscription plan categories (e.g.,                                     analytics plans, advertising plans, etc.)",
                max_length=24,
            ),
        ),
    ]