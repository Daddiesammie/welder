# Generated by Django 5.1.4 on 2024-12-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterequest',
            name='status_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='quoterequest',
            name='tracking_id',
            field=models.CharField(editable=False, max_length=12, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='quoterequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Review'), ('in_progress', 'In Progress'), ('approved', 'Quote Approved'), ('declined', 'Quote Declined'), ('completed', 'Project Completed')], default='pending', max_length=20),
        ),
    ]
