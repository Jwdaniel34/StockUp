# Generated by Django 2.1.5 on 2020-07-23 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_userstockportfolio_pay_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStockProfitTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_gained', models.FloatField(blank=True, null=True)),
                ('roi', models.FloatField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Profile')),
            ],
        ),
    ]
