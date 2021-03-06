# Generated by Django 2.2.1 on 2019-06-02 07:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=10, verbose_name='スラグ')),
                ('board_size', models.PositiveIntegerField(help_text='この数は偶数でなければなりません', validators=[django.core.validators.MinValueValidator(8), django.core.validators.MaxValueValidator(16)], verbose_name='盤面の大きさ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日')),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.Game', verbose_name='ゲーム')),
            ],
        ),
    ]
