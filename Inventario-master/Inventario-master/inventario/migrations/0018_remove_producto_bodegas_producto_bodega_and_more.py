# Generated by Django 4.2.3 on 2023-10-18 20:54

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0017_alter_perfilusuario_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='bodegas',
        ),
        migrations.AddField(
            model_name='producto',
            name='bodega',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventario.bodega'),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Usuario'),
        ),
    ]
