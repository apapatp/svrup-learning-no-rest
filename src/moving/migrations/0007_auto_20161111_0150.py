# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0006_auto_20161111_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='slug',
            field=models.SlugField(null=True, default=b'move', blank=True, unique=True),
            preserve_default=True,
        ),
    ]
