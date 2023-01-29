from django.contrib import admin
from .models import (
    PortfolioUser, SkillCategory, Skill, UserSkill, PortfolioUserSocialMediaLink,
    Review, NewClient, PortfolioUserAddress, ClientLead, ClientProject
)

# Register your models here.

admin.site.register(PortfolioUser)
admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(PortfolioUserSocialMediaLink)
admin.site.register(Review)
admin.site.register(NewClient)
admin.site.register(PortfolioUserAddress)
admin.site.register(ClientLead)
admin.site.register(ClientProject)
