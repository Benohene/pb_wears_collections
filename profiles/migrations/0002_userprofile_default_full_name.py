# Generated by Django 4.2.3 on 2023-08-16 00:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="default_full_name",
            field=models.CharField(
                blank=True, max_length=50, null=True
            ),
        ),
    ]
