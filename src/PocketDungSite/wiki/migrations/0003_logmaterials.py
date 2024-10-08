# Generated by Django 4.2.14 on 2024-08-14 20:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_material_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_name', models.CharField(max_length=300, verbose_name='Название материала (например спрайт, анимаци ходьбы, звук)')),
                ('ml_i_id', models.IntegerField(verbose_name='id статьи к которой идет материал')),
                ('ml_action', models.CharField(max_length=300, verbose_name='Название действия с файлом')),
                ('ml_date_add', models.DateField(default=datetime.date.today, verbose_name='Дата')),
                ('user_id', models.IntegerField(verbose_name='id пользователя')),
            ],
        ),
    ]
