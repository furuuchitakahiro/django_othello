# Generated by Django 2.2.1 on 2019-06-02 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matchings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matching',
            name='gest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='ゲスト'),
        ),
        migrations.AddField(
            model_name='matching',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='ホスト'),
        ),
    ]
