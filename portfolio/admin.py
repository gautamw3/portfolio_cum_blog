from django.contrib import admin
from .models import PortfolioUser, SkillCategory, Skill, UserSkill, PortfolioUserSocialMediaLink

# Register your models here.

admin.site.register(PortfolioUser)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(PortfolioUserSocialMediaLink)
