# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-14 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20170910_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='buyerPaysSalesTax',
            field=models.BooleanField(default=False, verbose_name='Buyer pays sales tax'),
        ),
    ]
