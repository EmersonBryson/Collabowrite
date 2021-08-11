# Generated by Django 2.2.4 on 2021-04-01 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collabowrite_app', '0003_auto_20210401_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_title', models.CharField(max_length=100)),
                ('section_summary', models.CharField(max_length=255)),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='collabowrite_app.Board')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='collabowrite_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=100)),
                ('post_content', models.CharField(max_length=500)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='collabowrite_app.Section')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='collabowrite_app.User')),
            ],
        ),
    ]