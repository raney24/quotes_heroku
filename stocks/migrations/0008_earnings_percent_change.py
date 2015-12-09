# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_auto_20151126_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='earnings',
            name='percent_change',
            field=models.DecimalField(default=1, max_digits=3, decimal_places=2),
            preserve_default=False,
        ),
    ]
