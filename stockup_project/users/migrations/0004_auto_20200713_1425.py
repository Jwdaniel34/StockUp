# Generated by Django 2.1.5 on 2020-07-13 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200713_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstockportfolio',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Profile'),
        ),
    ]