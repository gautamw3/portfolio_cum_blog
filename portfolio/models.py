from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField


class PortfolioUser(models.Model):
    """
    Model which stores the basic details of a registered user
    """
    WORK_DAYS = (
        ('1', 'Mon to Friday'),
        ('2', 'Mon to Saturday')
    )

    WORK_SHIFT = (
        ('1', '9 AM to 6 PM'),
        ('2', '10 AM to 7 PM'),
        ('3', '2:30 PM to 11:30 PM')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_portfolio')
    role = models.CharField(max_length=100, null=False, blank=False)
    profile_short_description = models.TextField()
    mobile = models.CharField(max_length=10, null=False, blank=False)
    heading = models.CharField(max_length=100, null=False, blank=False)
    headline = models.CharField(max_length=222, null=False, blank=False)
    about = FroalaField()
    profile_photo = models.ImageField(upload_to='portfolio/profile_photo')
    work_days = models.CharField(max_length=1, choices=WORK_DAYS)
    work_shift = models.CharField(max_length=1, choices=WORK_SHIFT)
    is_blogger = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Portfolio User'
        verbose_name_plural = 'Portfolio Users'


class PortfolioUserAddress(models.Model):
    """
    Stores and manages the address details of users
    """
    user = models.ForeignKey(PortfolioUser, on_delete=models.CASCADE, related_name='user_address')
    country = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'{self.user.user.first_name} {self.user.user.last_name} | {self.country} | {self.state} | {self.city}'

    class Meta:
        verbose_name = 'Portfolio User Address'
        verbose_name_plural = 'Portfolio User Addresses'


class PortfolioUserSocialMediaLink(models.Model):
    """
    Stores and manages various social media links associated with a user
    """
    user = models.ForeignKey(PortfolioUser, on_delete=models.CASCADE, related_name='user_social_links')
    github = models.CharField(max_length=222)
    linkedin = models.CharField(max_length=222)
    tweeter = models.CharField(max_length=222)
    instagram = models.CharField(max_length=222)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.user.first_name} {self.user.user.last_name} | Github: {self.github} | LinkedIn: {self.linkedin} | Tweeter: {self.tweeter} ' \
               f'| Instagram: {self.instagram}'

    class Meta:
        verbose_name = 'Social media link'
        verbose_name_plural = 'Social media links'


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
        ('DVPS', 'DevOps'),
        ('VCS', 'Version Control System'),
        ('AGIL', 'Agile Development Tools')
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
    STAR_RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    TOTAL_EXPERIENCE = (
        ('1', '1 Year'),
        ('2', '2 Years'),
        ('3', '3 Years'),
        ('4', '4 Years'),
        ('5', '5 Years'),
        ('6', '6 Years'),
        ('7', '7 Years'),
        ('8', '8 Years'),
        ('9', '9 Years'),
        ('10', '10 Years'),
        ('11', '11 Years'),
        ('12', '12 Years'),
        ('13', '13 Years'),
        ('14', '14 Years'),
        ('15', '15 Years'),
        ('16', '16 Years'),
        ('17', '17 Years'),
        ('18', '18 Years'),
        ('19', '19 Years'),
        ('20', '20 Years'),
        ('20+', '20+ Years'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_of_user')
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skill_category')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_desc')
    summary = models.CharField(max_length=222, null=False, blank=False)
    description = FroalaField()
    rating_out_of_five = models.CharField(max_length=1, null=False, blank=False, choices=STAR_RATINGS)
    total_experience_in_year = models.CharField(max_length=10, null=False, blank=False, choices=TOTAL_EXPERIENCE)
    using_since = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} | {self.skill_category.get_category_name_display()} | ' \
               f'{self.skill.category_item_name}'

    class Meta:
        verbose_name = 'User Skill'
        verbose_name_plural = 'User Skills'


class Review(models.Model):
    """
    Stores and manages the customer reviews
    """
    reviewer_name = models.CharField(max_length=100, null=False, blank=False)
    reviewer_rating = models.CharField(max_length=1, null=False, blank=False, choices=UserSkill.STAR_RATINGS)
    review_description = FroalaField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reviewer_name

    class Meta:
        verbose_name = 'Customer Review'
        verbose_name_plural = 'Customer Reviews'


class NewClient(models.Model):
    """ Stores the email addresses of the new clients who came across the application and shown interest """
    client_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_email

    class Meta:
        verbose_name = 'Client email'
        verbose_name_plural = 'Client emails'


class ClientLead(models.Model):
    """
    Stores and manages the client leads generated by contact us form
    """
    client_name = models.CharField(max_length=100, null=False, blank=False)
    client_email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(null=False, blank=False, max_length=222)
    message = FroalaField()
    file_supporting_the_message = models.FileField(upload_to='portfolio/client_lead', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.client_name} | {self.client_email}'

    class Meta:
        verbose_name = 'Client lead'
        verbose_name_plural = 'Client leads'


class ClientProject(models.Model):
    """
    Stores and manages all the information about the client projects user has done so far
    """
    user = models.ForeignKey(PortfolioUser, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    project_url = models.URLField(null=True, blank=True)
    tools_and_technologies_used = models.ManyToManyField(UserSkill, related_name='tools_and_technologies_used')
    project_description = FroalaField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.user.first_name} {self.user.user.first_name} | {self.project_title} | {self.client_name}'

    class Meta:
        verbose_name = 'Client project'
        verbose_name_plural = 'Client projects'
