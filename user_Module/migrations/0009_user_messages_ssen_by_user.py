# Generated by Django 4.2 on 2023-12-14 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_Module', '0008_user_messages_creation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_messages',
            name='ssen_by_user',
            field=models.BooleanField(default=False, verbose_name='خوانده شده'),
        ),
    ]