# Generated by Django 4.2.3 on 2023-10-18 02:29

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0015_alter_perfilusuario_username_alter_producto_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodega',
            name='direccion',
            field=models.CharField(default='Valor predeterminado', max_length=50),
        ),
        migrations.AlterField(
            model_name='bodega',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='rol',
            field=models.CharField(choices=[('JF', 'Jefe de Bodega'), ('BD', 'Bodeguero')], default='BD', max_length=50),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(400)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(50)]),
        ),
    ]