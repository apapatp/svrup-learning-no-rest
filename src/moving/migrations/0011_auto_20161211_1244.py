# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moving', '0010_auto_20161124_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'ordering': ['title', 'timestamp']},
        ),
        migrations.AddField(
            model_name='move',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
