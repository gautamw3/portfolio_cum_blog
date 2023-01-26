from django.db import models
from django.contrib.auth.models import User


class PortfolioUser(models.Model):
    """
    Model which stores the basic details of a registered user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_portfolio')
    mobile = models.CharField(max_length=10, null=False, blank=False)
    heading = models.CharField(max_length=100, null=False, blank=False)
    headline = models.CharField(max_length=222, null=False, blank=False)
    about = models.TextField()
    profile_photo = models.ImageField(upload_to='portfolio/profile_photo')
    is_blogger = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Portfolio User'
        verbose_name_plural = 'Portfolio Users'


class SkillCategory(models.Model):
    """
    Model which stores all the skills category
    """
    SKILL_CATEGORIES = (
        ('PLBE', 'Backend Programming languages'),
        ('PLFE', 'Frontend Programming languages'),
        ('DBMS', 'Databases'),
        ('OPRS', 'Operating systems'),
        ('MCHL', 'Machine learning'),
        ('NLPR', 'Natural language processing'),
        ('WEBT', 'Web Technologies'),
    )

    category_name = models.CharField(max_length=4, choices=SKILL_CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.get_category_name_display()}'

    class Meta:
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'


class Skill(models.Model):
    """
    Model which holds all the skills category items
    """
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='category_of_skill')
    category_item_name = models.CharField(max_length=100, null=False, blank=False)
    category_item_image = models.ImageField(upload_to='portfolio/skill_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.category_item_name} | {self.skill_category.get_category_name_display()}'

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class UserSkill(models.Model):
    """
    Model which holds each user's skills information
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_of_user')
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skill_category')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_desc')
    summary = models.CharField(max_length=222, null=False, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} | {self.skill_category.get_category_name_display()} | ' \
               f'{self.skill.category_item_name}'

    class Meta:
        verbose_name = 'User Skill'
        verbose_name_plural = 'User Skills'
