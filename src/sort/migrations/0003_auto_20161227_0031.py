# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sort', '0002_auto_20161227_0008'),
    ]

    operations = [
        migrations.CreateModel(
            name='SortLocationItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=b'images/', blank=True)),
                ('slug', models.SlugField(default=b'room', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='sortlocation',
            name='item',
            field=models.ForeignKey(related_name='sort_location_item', default=None, to='sort.SortLocationItem'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sortlocation',
            name='name',
            field=models.CharField(default=(b'kitchen', b'kitchen'), max_length=255),
            preserve_default=True,
        ),
    ]
