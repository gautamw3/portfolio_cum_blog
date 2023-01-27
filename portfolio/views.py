from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import PortfolioUser, UserSkill, Skill, SkillCategory, PortfolioUserSocialMediaLink


class GlobalResponse:
    """
    Returns global response object
    """
    def __init__(self):
        self.response_data = response_data = {
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
        self.pk = 8
        self.user_model = user_model
        self.user_obj = None

    def get_user_obj(self):
        self.user_obj = self.user_model.objects.get(pk=8)
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


def index(request):
    template = 'portfolio/index.html'
    try:
        if request.user.is_authenticated:
            obj_user = User.objects.get(pk=request.user.id)
            obj_portfolio_user = PortfolioUser.objects.get(pk=obj_user.user_portfolio.id)
        else:
            obj_user = get_global_user(request)
            obj_portfolio_user = PortfolioUser.objects.get(user__id=obj_user.id)
        obj_user_skills = UserSkill.objects.filter(user__id=obj_user.id)
        skills = {}
        for each_item in obj_user_skills:
            if each_item.skill_category.get_category_name_display() in skills:
                skills[each_item.skill_category.get_category_name_display()].append(
                    {
                        each_item.skill.category_item_name: {
                            'id': each_item.skill.id,
                            'summary': each_item.summary,
                            'description': each_item.description,
                            'logo': each_item.skill.category_item_image.url
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
                            'logo': each_item.skill.category_item_image.url
                        }
                    }
                ]
        heading = obj_portfolio_user.heading
        headline = obj_portfolio_user.headline
        about = obj_portfolio_user.about
        profile_photo = obj_portfolio_user.profile_photo.url
        obj_social_links = PortfolioUserSocialMediaLink.objects.get(user_id=obj_portfolio_user.id)
        context = {
            'page_title': 'Home',
            'heading': heading,
            'headline': headline,
            'profile_photo': profile_photo,
            'about': about,
            'linkedin': obj_social_links.linkedin,
            'tweeter': obj_social_links.tweeter,
            'instagram': obj_social_links.instagram,
            'skills': skills
        }
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
            obj_user_social_link = PortfolioUserSocialMediaLink.objects.get(user_id=obj_user.user_portfolio.id)
            context['page_details']['linkedin'] = obj_user_social_link.linkedin
            context['page_details']['tweeter'] = obj_user_social_link.tweeter
            context['page_details']['instagram'] = obj_user_social_link.instagram
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
            context['page_details']['using_since'] = obj_tech_details.using_since
            context['page_details']['image'] = obj_tech_details.skill.category_item_image.url
        else:
            context['error'] = f'Invalid request method: {request.method}!'
    except Exception as err:
        context['page_details'] = None
        context['exception'] = err.__str__()
    return render(request, template, context)
