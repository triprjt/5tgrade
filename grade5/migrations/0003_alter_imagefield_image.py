# Generated by Django 4.2.4 on 2023-08-29 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("grade5", "0002_imagefield_mcq_textfield_videofield_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="imagefield",
            name="image",
            field=models.JSONField(blank=True, null=True),
        ),
    ]