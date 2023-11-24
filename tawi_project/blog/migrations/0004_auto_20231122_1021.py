# Generated by Django 3.2.16 on 2023-11-22 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20231122_1021'),
        ('blog', '0003_resume'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Resume',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
        ),
    ]
