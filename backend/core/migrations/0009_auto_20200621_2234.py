# Generated by Django 2.2.13 on 2020-06-21 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200621_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='state',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]