# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0002_remove_type_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='slug',
            field=models.SlugField(default=b'abc', unique=True),
            preserve_default=True,
        ),
    ]
