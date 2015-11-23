# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_remove_stock_current_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='earnings',
            name='er_quarter',
            field=models.TextField(default=b'Q1'),
        ),
    ]
