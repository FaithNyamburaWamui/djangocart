# Generated by Django 5.1.1 on 2024-09-18 13:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeowner', '0001_initial'),
        ('material', '0002_alter_material_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='homeowner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='material', to='homeowner.homeowner'),
            preserve_default=False,
        ),
    ]
