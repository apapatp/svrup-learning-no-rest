# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_auto_20161212_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 12, 8, 40, 5, 403461, tzinfo=utc), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 12, 8, 40, 5, 404060, tzinfo=utc), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.CharField(unique=True, max_length=120),
            preserve_default=True,
        ),
    ]
