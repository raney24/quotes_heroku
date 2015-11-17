# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Earnings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('before_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('after_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('er_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('symbol', models.CharField(max_length=5, verbose_name=b'Stock Symbol')),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('last_accessed', models.DateTimeField(auto_now_add=True)),
                ('current_price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.AddField(
            model_name='earnings',
            name='stock',
            field=models.ForeignKey(to='stocks.Stock'),
        ),
    ]
