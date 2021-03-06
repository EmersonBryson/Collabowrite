# Generated by Django 2.2.4 on 2021-03-31 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collabowrite_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_title', models.CharField(max_length=50)),
                ('board_topic', models.CharField(max_length=30)),
                ('board_tags', models.CharField(max_length=100)),
                ('board_image', models.ImageField(upload_to='boards')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='collabowrite_app.User')),
            ],
        ),
    ]
