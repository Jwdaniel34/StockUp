# Generated by Django 2.1.5 on 2020-07-13 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200713_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstockportfolio',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Profile'),
        ),
    ]
