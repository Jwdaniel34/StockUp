# Generated by Django 2.1.5 on 2020-06-30 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='home/static/img/profileImg.png', upload_to='users/%Y/%m/%d/'),
        ),
    ]