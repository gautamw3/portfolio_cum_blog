# Generated by Django 4.1.5 on 2023-01-28 12:44

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0017_alter_clientlead_file_supporting_the_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientlead',
            name='message',
            field=froala_editor.fields.FroalaField(),
        ),
    ]
