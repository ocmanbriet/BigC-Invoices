# Generated by Django 4.1.3 on 2023-11-08 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_orders_billing_phone_alter_orders_billing_zip_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="orders",
            name="company_name",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
