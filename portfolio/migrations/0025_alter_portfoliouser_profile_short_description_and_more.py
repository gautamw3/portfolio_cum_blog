# Generated by Django 4.1.5 on 2023-01-29 11:40

from django.db import migrations, models
import django.db.models.deletion
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0024_alter_skillcategory_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliouser',
            name='profile_short_description',
            field=froala_editor.fields.FroalaField(),
        ),
        migrations.CreateModel(
            name='ClientProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=100)),
                ('project_url', models.URLField()),
                ('project_description', froala_editor.fields.FroalaField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tools_and_technologies_used', models.ManyToManyField(to='portfolio.userskill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfoliouser')),
            ],
            options={
                'verbose_name': 'Client project',
                'verbose_name_plural': 'Client projects',
            },
        ),
    ]
