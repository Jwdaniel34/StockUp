# Generated by Django 2.1.5 on 2020-06-30 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200630_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='home/static/home/img/profileimg.png', upload_to='users/%Y/%m/%d/'),
        ),
    ]