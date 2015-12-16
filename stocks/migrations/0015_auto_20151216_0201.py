# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0014_auto_20151211_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='symbol',
            field=models.CharField(unique=True, max_length=5, verbose_name=b'Stock Symbol'),
        ),
    ]
