# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0005_move_share_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='slug',
            field=models.SlugField(default=b'move', null=True, blank=True),
            preserve_default=True,
        ),
    ]
