# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0009_auto_20151208_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='percent_change',
            field=models.DecimalField(null=True, max_digits=11, decimal_places=2),
        ),
    ]
