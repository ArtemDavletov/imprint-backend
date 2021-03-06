# Generated by Django 3.2.5 on 2021-07-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("browser", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="screenresolution",
            name="landscape",
            field=models.NullBooleanField(default=None, verbose_name="Land Scape"),
        ),
        migrations.RemoveField(
            model_name="configurations",
            name="donottrack",
        ),
        migrations.AddField(
            model_name="configurations",
            name="donottrack",
            field=models.NullBooleanField(default=None, verbose_name="Do Not Track"),
        ),
        migrations.RemoveField(
            model_name="configurations",
            name="hardwareconcurrency",
        ),
        migrations.AddField(
            model_name="configurations",
            name="hardwareconcurrency",
            field=models.CharField(
                default=1, max_length=200, verbose_name="HardwareConcurrency"
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="configurations",
            name="memory",
        ),
        migrations.AddField(
            model_name="configurations",
            name="memory",
            field=models.CharField(default=1, max_length=20, verbose_name="memory"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="instancebrowser",
            name="donottrack",
            field=models.NullBooleanField(
                default=None, max_length=20, verbose_name="Do Not Track"
            ),
        ),
        migrations.DeleteModel(
            name="DoNotTrack",
        ),
        migrations.DeleteModel(
            name="HardwareConcurrency",
        ),
        migrations.DeleteModel(
            name="Memory",
        ),
    ]
