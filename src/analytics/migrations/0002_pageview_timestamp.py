# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='timestamp',
            field=models.DateField(default=datetime.datetime(2016, 12, 11, 21, 10, 22, 463412, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
