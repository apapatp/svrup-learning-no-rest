# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0011_auto_20161211_1244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='move',
            options={'ordering': ['order', '-timestamp']},
        ),
    ]
