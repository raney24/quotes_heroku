# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0008_earnings_percent_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='percent_change',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=2),
        ),
    ]
