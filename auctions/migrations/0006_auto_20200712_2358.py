# Generated by Django 3.0.6 on 2020-07-12 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200712_2351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='title',
            new_name='item',
        ),
    ]