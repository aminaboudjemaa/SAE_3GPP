# Generated by Django 5.1.7 on 2025-03-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('tdoc_id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('source', models.CharField(blank=True, max_length=500, null=True)),
                ('contact', models.CharField(blank=True, max_length=500, null=True)),
                ('contact_id', models.CharField(blank=True, max_length=500, null=True)),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
                ('doc_for', models.CharField(blank=True, max_length=500, null=True)),
                ('abstract', models.CharField(blank=True, max_length=500, null=True)),
                ('secretary_remarks', models.CharField(blank=True, max_length=500, null=True)),
                ('agenda_item_sort_order', models.CharField(blank=True, max_length=500, null=True)),
                ('agenda_item', models.CharField(blank=True, max_length=500, null=True)),
                ('agenda_item_description', models.CharField(blank=True, max_length=500, null=True)),
                ('tdoc_sort_order_within_agenda_item', models.CharField(blank=True, max_length=500, null=True)),
                ('tdoc_status', models.CharField(blank=True, max_length=500, null=True)),
                ('reservation_date', models.CharField(blank=True, max_length=500, null=True)),
                ('uploaded', models.CharField(blank=True, max_length=500, null=True)),
                ('is_revision_of', models.CharField(blank=True, max_length=500, null=True)),
                ('revised_to', models.CharField(blank=True, max_length=500, null=True)),
                ('release', models.CharField(blank=True, max_length=500, null=True)),
                ('spec', models.CharField(blank=True, max_length=500, null=True)),
                ('version', models.CharField(blank=True, max_length=500, null=True)),
                ('related_wis', models.CharField(blank=True, max_length=500, null=True)),
                ('cr', models.CharField(blank=True, max_length=500, null=True)),
                ('cr_revision', models.CharField(blank=True, max_length=500, null=True)),
                ('cr_category', models.CharField(blank=True, max_length=500, null=True)),
                ('tsg_cr_pack', models.CharField(blank=True, max_length=500, null=True)),
                ('reply_to', models.CharField(blank=True, max_length=500, null=True)),
                ('to', models.CharField(blank=True, max_length=500, null=True)),
                ('cc', models.CharField(blank=True, max_length=500, null=True)),
                ('original_ls', models.CharField(blank=True, max_length=500, null=True)),
                ('reply_in', models.CharField(blank=True, max_length=500, null=True)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('topic', models.CharField(blank=True, max_length=500, null=True)),
                ('problem', models.CharField(blank=True, max_length=500, null=True)),
                ('solution', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'documents',
            },
        ),
    ]
