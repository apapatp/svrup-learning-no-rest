# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0004_auto_20161021_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='share_message',
            field=models.TextField(default=b'check out maneuverbuddy'),
            preserve_default=True,
        ),
    ]
