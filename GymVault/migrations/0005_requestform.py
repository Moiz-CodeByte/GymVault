# Generated by Django 5.2.2 on 2025-06-11 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymvault', '0004_member_is_active_member_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('message', models.TextField()),
                ('status', models.CharField(default='pending', max_length=20)),
            ],
        ),
    ]
