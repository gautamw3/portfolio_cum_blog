# Generated by Django 4.1.5 on 2023-01-28 13:05

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0018_alter_clientlead_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliouser',
            name='about',
            field=froala_editor.fields.FroalaField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_description',
            field=froala_editor.fields.FroalaField(),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='description',
            field=froala_editor.fields.FroalaField(),
        ),
    ]