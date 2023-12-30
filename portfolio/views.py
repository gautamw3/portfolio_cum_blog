from django.http import JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import get_template
from portfolio_cum_blog import settings
from .models import (
    PortfolioUser, UserSkill, PortfolioUserSocialMediaLink, Review, NewClient, PortfolioUserAddress, ClientProject
)
from .forms import ContactUs


class GlobalResponse:
    """
    Returns global response object
    """
    def __init__(self):
        self.response_data = {
            'response': '',
            'responseMessage': '',
            'responseMessageInfo': ''
        }

    def get_response_obj(self):
        return self.response_data


class GlobalUser:
    """
    Returns global user object
    """
    def __init__(self, user_model):
        self.pk = settings.DEFAULT_USER
        self.user_model = user_model
        self.user_obj = None

    def get_user_obj(self):
        self.user_obj = self.user_model.objects.get(pk=self.pk)
        return self.user_obj


def get_global_response(request):
    """
    Returns global response object
    """
    global_response_obj = GlobalResponse()
    response_data = global_response_obj.get_response_obj()
    return response_data


def get_global_user(request):
    """
    Returns global user object
    """
    global_user_obj = GlobalUser(User)
    obj_user = global_user_obj.get_user_obj()
    return obj_user


def get_user_skills(user_id):
    """
    Returns all the skills mapped to a user
    """
    obj_user_skills = UserSkill.objects.filter(user__id=user_id)
    skills = {}
    for each_item in obj_user_skills:
        rating = int(each_item.get_rating_out_of_five_display())
        if rating == 5:
            progress_bar_color = 1
        elif rating == 4:
            progress_bar_color = 7
        elif rating == 3:
            progress_bar_color = 4
        elif rating == 2:
            progress_bar_color = 3
        else:
            progress_bar_color = 2
        if each_item.skill_category.get_category_name_display() in skills:
            skills[each_item.skill_category.get_category_name_display()].append(
                {
                    each_item.skill.category_item_name: {
                        'id': each_item.skill.id,
                        'summary': each_item.summary,
                        'description': each_item.description,
                        'logo': each_item.skill.category_item_image.url,
                        'total_experience_in_year': each_item.get_total_experience_in_year_display(),
                        'rating_out_of_five': rating * 20,
                        'progress_bar_color': progress_bar_color
                    }
                }
            )
        else:
            skills[each_item.skill_category.get_category_name_display()] = [
                {
                    each_item.skill.category_item_name: {
                        'id': each_item.skill.id,
                        'summary': each_item.summary,
                        'description': each_item.description,
                        'logo': each_item.skill.category_item_image.url,
                        'total_experience_in_year': each_item.get_total_experience_in_year_display(),
                        'rating_out_of_five': rating * 20,
                        'progress_bar_color': progress_bar_color
                    }
                }
            ]
    return skills


def get_customer_reviews():
    obj_customer_reviews = Review.objects.all()
    customer_reviews = []
    for each_review in obj_customer_reviews:
        customer_review = {
            'reviewer': each_review.reviewer_name,
            'rating': [i for i in range(int(each_review.get_reviewer_rating_display()))],
            'description': each_review.review_description
        }
        customer_reviews.append(customer_review)
    return customer_reviews


def get_social_media_links(portfolio_user_id):
    try:
        obj_social_media_links = PortfolioUserSocialMediaLink.objects.get(user_id=portfolio_user_id)
    except Exception as err:
        obj_social_media_links = None
    return obj_social_media_links


def embed_social_media_links_to_context(context, obj_social_media_links):
    if obj_social_media_links is not None:
        context['github'] = obj_social_media_links.github
        context['linkedin'] = obj_social_media_links.linkedin
        context['tweeter'] = obj_social_media_links.tweeter
        context['instagram'] = obj_social_media_links.instagram
    return context


def index(request):
    template = 'portfolio/index.html'
    try:
        if request.user.is_authenticated:
            obj_user = User.objects.get(pk=request.user.id)
            obj_portfolio_user = PortfolioUser.objects.get(pk=obj_user.user_portfolio.id)
        else:
            obj_user = get_global_user(request)
            obj_portfolio_user = PortfolioUser.objects.get(pk=obj_user.user_portfolio.id)
        customer_reviews = get_customer_reviews()
        skills = get_user_skills(obj_user.id)
        heading = obj_portfolio_user.heading
        headline = obj_portfolio_user.headline
        about = obj_portfolio_user.about
        profile_photo = obj_portfolio_user.profile_photo.url
        obj_social_media_links = get_social_media_links(obj_portfolio_user.id)
        context = {
            'page_title': 'Home',
            'heading': heading,
            'headline': headline,
            'profile_photo': profile_photo,
            'about': about,
            'skills': skills,
            'customer_reviews': customer_reviews
        }
        context = embed_social_media_links_to_context(context, obj_social_media_links)
    except Exception as err:
        context = {
            'page_title': 'Home',
            'exception': err.__str__()
        }
    return render(request, template, context)


def user_signup(request):
    """
    Registers the user with the system
    """
    response_data = get_global_response(request)
    try:
        if request.method == 'POST':
            first_name = request.POST['firstName']
            last_name = request.POST['lastName']
            user_email = request.POST['userMail']
            user_mobile = request.POST['userMobile']
            user_password = request.POST['password']
            if first_name and last_name and user_email and user_mobile and user_password:
                user = User.objects.create_user(
                    username=user_email,
                    email=user_email,
                    password=user_password
                )
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                obj_portfolio_user = PortfolioUser(
                    user=user,
                    mobile=user_mobile,
                )
                obj_portfolio_user.save()
                user = authenticate(username=user_email, password=user_password)
                if user is not None:
                    login(request, user)
                response_data['response'] = 'success'
                response_data['responseMessage'] = 'You have been registered successfully'
                response_data['responseMessageInfo'] = 'Redirecting to the dashboard'
            else:
                response_data['response'] = 'error'
                response_data['responseMessage'] = 'Registration Failed'
                response_data['responseMessageInfo'] = f'Invalid HTTP method {request.method}'
        else:
            response_data['response'] = 'warning'
            response_data['responseMessage'] = 'Registration Failed'
            response_data['responseMessageInfo'] = 'Invalid input/please check if each and every mandatory details' \
                                                   'were provided or not!'
    except Exception as err:
        response_data['response'] = 'error'
        response_data['responseMessage'] = 'Registration Failed'
        response_data['responseMessageInfo'] = str(err)
    return JsonResponse(response_data)


def user_login(request):
    """
    Lets the user login to the application
    """
    response_data = get_global_response(request)
    try:
        if request.method == 'POST':
            user_email = request.POST['userMailSignIn']
            user_password = request.POST['passwordSignIn']
            if user_email and user_password:
                user = authenticate(username=user_email, password=user_password)
                if user is not None:
                    login(request, user)
                    response_data['response'] = 'success'
                    response_data['responseMessage'] = 'Login successful'
                    response_data['responseMessageInfo'] = 'Redirecting to the dashboard'
                else:
                    response_data['response'] = 'error'
                    response_data['responseMessage'] = 'Login failed'
                    response_data['responseMessageInfo'] = 'Invalid user'
        else:
            response_data['response'] = 'error'
            response_data['responseMessage'] = 'Login failed'
            response_data['responseMessageInfo'] = f'Invalid HTTP method {request.method}'
    except Exception as err:
        response_data['response'] = 'error'
        response_data['responseMessage'] = 'Login failed'
        response_data['responseMessageInfo'] = str(err)
    return JsonResponse(response_data)


def user_logout(request):
    """
    Lets the logged-in user logout of the application
    """
    logout(request)
    return redirect(reverse('index'))


def tech_details(request, tech_id):
    """
    Loads the technology details page
    """
    template = 'portfolio/tech_details.html'
    context = {
        "page_title": "Technology details",
        "banner_heading_pref": "Technology",
        'page_details': {}
    }
    try:
        if request.method == "GET":
            if request.user.is_authenticated:
                user_id = request.user.id
                obj_user = User.objects.get(pk=user_id)
            else:
                obj_user = get_global_user(request)
            obj_tech_details = UserSkill.objects.get(user__id=obj_user.id, skill__id=tech_id)
            obj_social_media_links = get_social_media_links(obj_user.user_portfolio.id)
            context = embed_social_media_links_to_context(context, obj_social_media_links)
            breadcrumb_mid_item_cat_list = obj_tech_details.skill_category.get_category_name_display().split()
            if len(breadcrumb_mid_item_cat_list) > 1:
                context['page_details']['heading'] = f'{obj_tech_details.skill.category_item_name} ' \
                                                     f'{breadcrumb_mid_item_cat_list[0]} ' \
                                                     f'{breadcrumb_mid_item_cat_list[1]}'
            else:
                context['page_details']['heading'] = f'{obj_tech_details.skill.category_item_name} ' \
                                                     f'{obj_tech_details.skill_category.get_category_name_display()}'
            context['page_details']['breadcrumb_mid_item'] = obj_tech_details.skill.category_item_name
            context['page_details']['summary'] = obj_tech_details.summary
            context['page_details']['description'] = obj_tech_details.description
            context['page_details']['rating'] = [i for i in range(int(obj_tech_details.rating_out_of_five))]
            context['page_details']['total_experience'] = obj_tech_details.get_total_experience_in_year_display()
            context['page_details']['last_used'] = obj_tech_details.last_used
            context['page_details']['image'] = obj_tech_details.skill.category_item_image.url
        else:
            context['error'] = f'Invalid request method: {request.method}!'
    except Exception as err:
        context['page_details'] = None
        context['exception'] = err.__str__()
    return render(request, template, context)


def new_client_feed(request):
    """
    Stores the email address of the client who shown interest by submitting their email address
    """
    response_data = get_global_response(request)
    try:
        if request.method == 'POST':
            client_email = request.POST['new_client_email']
            obj_new_client_email = NewClient(client_email=client_email)
            obj_new_client_email.save()
            response_data['response'] = 'success'
            response_data['responseMessage'] = 'We got that'
            response_data['responseMessageInfo'] = 'Thanks for showing interest in availing our services'
        else:
            response_data['response'] = 'error'
            response_data['responseMessage'] = 'Something went wrong'
            response_data['responseMessageInfo'] = 'Invalid HTTP request'
    except Exception as err:
        pass
        response_data['response'] = 'error'
        response_data['responseMessage'] = err.__str__()
        response_data['responseMessageInfo'] = 'Please try after sometime'
    return JsonResponse(response_data)


def send_new_client_lead_mail(email_data):
    template = 'portfolio/email_templates/new_client_lead.html'
    message_to_attach = get_template(template).render(email_data)
    email_message = EmailMessage(
        "New client lead",
        message_to_attach,
        settings.APPLICATION_EMAIL,
        [email_data['client_email']],
        reply_to=[settings.APPLICATION_EMAIL]
    )
    email_message.content_subtype = 'html'
    email_message.send(fail_silently=False)


def contact_us(request):
    """
    Loads contact us page
    """
    template = 'portfolio/contact_us.html'
    context = {
        'page_title': 'Contact us'
    }
    try:
        if request.method == 'POST':
            form = ContactUs(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                email_data = {
                    'client_name': request.POST['client_name'],
                    'client_email': request.POST['client_email'],
                    'subject': request.POST['subject'],
                    'message': request.POST['message'],
                }
                send_new_client_lead_mail(email_data)
                context['response'] = 'success'
            else:
                context['response'] = 'error'
        else:
            form = ContactUs()

        if request.user.is_authenticated:
            obj_user = User.objects.get(pk=request.user.id)
        else:
            obj_user = get_global_user(request)
        try:
            obj_user_address = PortfolioUserAddress.objects.get(user_id=obj_user.user_portfolio.id)
        except PortfolioUserAddress.DoesNotExist:
            obj_user_address = None
        obj_social_media_links = get_social_media_links(obj_user.user_portfolio.id)
        context = embed_social_media_links_to_context(context, obj_social_media_links)
        if obj_user_address is not None:
            context['country'] = obj_user_address.country
            context['state'] = obj_user_address.state
            context['city'] = obj_user_address.city
            context['mobile'] = obj_user.user_portfolio.mobile
            context['email'] = obj_user.email
            context['work_days'] = obj_user.user_portfolio.get_work_days_display()
            context['work_shift'] = obj_user.user_portfolio.get_work_shift_display()
        context['form'] = form
    except Exception as err:
        context['exception'] = err.__str__()
    return render(request, template, context)


def about_me(request):
    """
    Renders the about page
    """
    template = 'portfolio/about-me.html'
    context = {
        "page_title": "About me",
    }
    try:
        if request.method == "GET":
            if request.user.is_authenticated:
                user_id = request.user.id
                obj_user = User.objects.get(pk=user_id)
            else:
                obj_user = get_global_user(request)
            context['about'] = obj_user.user_portfolio.about
            context['profile_photo'] = obj_user.user_portfolio.profile_photo.url
            obj_customer_reviews = Review.objects.all()
            customer_reviews = []
            for each_review in obj_customer_reviews:
                customer_review = {
                    'reviewer': each_review.reviewer_name,
                    'rating': [i for i in range(int(each_review.get_reviewer_rating_display()))],
                    'description': each_review.review_description
                }
                customer_reviews.append(customer_review)
            obj_social_media_links = get_social_media_links(obj_user.user_portfolio.id)
            context = embed_social_media_links_to_context(context, obj_social_media_links)
            context['customer_reviews'] = customer_reviews
        else:
            context['error'] = 'Invalid HTTP method detected'
    except Exception as err:
        context['exception'] = err.__str__()
    return render(request, template, context)


def user_portfolio(request):
    """
    Loads the portfolio page
    """
    template = 'portfolio/portfolio.html'
    context = {
        'page_title': 'User Portfolio'
    }
    try:
        if request.method == 'GET':
            if request.user.is_authenticated:
                obj_user = User.objects.get(pk=request.user.id)
            else:
                obj_user = get_global_user(request)
            obj_social_media_links = get_social_media_links(obj_user.user_portfolio.id)
            skills = get_user_skills(obj_user.id)
            context['heading'] = obj_user.user_portfolio.heading
            context['headline'] = obj_user.user_portfolio.headline
            context['skills'] = skills
            context = embed_social_media_links_to_context(context, obj_social_media_links)
        else:
            context['error'] = 'Invalid HTTP method detected'
    except Exception as err:
        context['exception'] = err.__str__()
    return render(request, template, context)


def user_profile_details(request, user_id):
    """
    Loads user profile details page
    """
    template = 'portfolio/profile_details.html'
    context = {
        'page_title': 'Profile details'
    }
    try:
        if request.method == 'GET':
            obj_portfolio_user = PortfolioUser.objects.get(user_id=user_id)
            obj_social_media_links = get_social_media_links(obj_portfolio_user.id)
            skills = get_user_skills(user_id)
            obj_client_projects = ClientProject.objects.filter(user_id=obj_portfolio_user.id)
            client_project_list = []
            for each_client_project in obj_client_projects:
                tools_and_tech_list = []
                obj_tools_and_tech = each_client_project.tools_and_technologies_used.all()
                for each_tool_and_tech in obj_tools_and_tech:
                    tools_and_tech_list.append(each_tool_and_tech.skill.category_item_name)
                client_project_list.append(
                    {
                        'project_title': each_client_project.project_title,
                        'client_name': each_client_project.client_name,
                        'project_url': each_client_project.project_url,
                        'tools_and_technologies_used': tools_and_tech_list,
                        'project_description': each_client_project.project_description
                    }
                )
            context['client_project_list'] = client_project_list
            context['role'] = obj_portfolio_user.role
            context['profile_short_description'] = obj_portfolio_user.profile_short_description
            context['mobile'] = obj_portfolio_user.mobile
            context['email'] = obj_portfolio_user.user.email
            context['about'] = obj_portfolio_user.about
            context['profile_photo'] = obj_portfolio_user.profile_photo.url
            context['user_first_name'] = obj_portfolio_user.user.first_name
            context['skills'] = skills
            context = embed_social_media_links_to_context(context, obj_social_media_links)
        else:
            context['error'] = 'Invalid HTTP method detected'
    except Exception as err:
        context['exception'] = err.__str__()
    return render(request, template, context)
