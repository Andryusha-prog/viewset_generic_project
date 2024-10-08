# Generated by Django 5.1.1 on 2024-10-09 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="link",
            field=models.CharField(
                blank=True, max_length=400, null=True, verbose_name="ссылка на оплату"
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(
                blank=True,
                max_length=300,
                null=True,
                verbose_name="идентификатор сессии",
            ),
        ),
    ]
