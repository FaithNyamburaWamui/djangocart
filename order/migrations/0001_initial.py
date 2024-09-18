# Generated by Django 5.1.1 on 2024-09-17 12:08

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.CharField(max_length=200)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='material.material')),
            ],
        ),
    ]
