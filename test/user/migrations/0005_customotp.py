# Generated by Django 4.0.10 on 2023-03-23 07:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_email_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomOtp',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=255)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
