# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0009_taggeditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.SlugField(choices=[(b'python', b'python'), (b'django', b'django'), (b'home', b'home'), (b'apartment', b'apartment'), (b'muscle', b'muscle')]),
            preserve_default=True,
        ),
    ]
