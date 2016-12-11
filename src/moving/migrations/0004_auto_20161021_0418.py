# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0003_type_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='slug',
            field=models.SlugField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='move',
            unique_together=set([('slug', 'move_type')]),
        ),
    ]
