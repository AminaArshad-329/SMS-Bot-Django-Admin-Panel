# Generated by Django 5.0.6 on 2024-06-02 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_user_location_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='inactive',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]