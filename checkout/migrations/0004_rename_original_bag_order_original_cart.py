# Generated by Django 4.2.3 on 2023-08-15 14:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0003_order_original_bag_order_stripe_pid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="original_bag",
            new_name="original_cart",
        ),
    ]
