# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20161125_0653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='unread',
        ),
    ]
