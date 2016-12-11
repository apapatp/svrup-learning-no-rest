# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_comment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(default=None, blank=True, to='comments.Comment', null=True),
            preserve_default=True,
        ),
    ]
