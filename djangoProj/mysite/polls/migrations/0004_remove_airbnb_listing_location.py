# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 09:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_remove_airbnb_listing_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airbnb_listing',
            name='location',
        ),
    ]