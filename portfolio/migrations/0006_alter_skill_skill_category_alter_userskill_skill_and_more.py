# Generated by Django 4.1.5 on 2023-01-26 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolio', '0005_alter_portfoliouser_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='skill_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_of_skill', to='portfolio.skillcategory'),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_desc', to='portfolio.skill'),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='skill_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_category', to='portfolio.skillcategory'),
        ),
        migrations.AlterField(
            model_name='userskill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_of_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
