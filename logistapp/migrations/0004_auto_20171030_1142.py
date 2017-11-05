# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 08:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logistapp', '0003_auto_20171030_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='address_from',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='from_post_office', to='logistapp.PostOffice'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='address_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='to_post_office', to='logistapp.PostOffice'),
            preserve_default=False,
        ),
    ]
