# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0007_auto_20161111_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='move_type',
            field=models.ForeignKey(blank=True, to='moving.Type', null=True),
            preserve_default=True,
        ),
    ]
