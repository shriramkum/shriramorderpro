# Generated by Django 3.2.3 on 2021-07-30 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'New'), (' in-process', 'In-Process'), ('complete', 'Complete')], default='new', max_length=100),
        ),
    ]
