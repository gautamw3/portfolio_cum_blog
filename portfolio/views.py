from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import PortfolioUser, UserSkill, Skill, SkillCategory
from portfolio_cum_blog import settings

response_data = {
        'response': '',
        'responseMessage': '',
        'responseMessageInfo': ''
    }


def index(request):
    template = 'portfolio/index.html'
    try:
        if request.user.is_authenticated:
            obj_user = User.objects.get(pk=request.user.id)
            obj_portfolio_user = PortfolioUser.objects.get(pk=obj_user.user_portfolio.id)
        else:
            obj_portfolio_user = PortfolioUser.objects.get(mobile='7764054938')
        obj_user_skills = UserSkill.objects.filter(user__id=obj_portfolio_user.user.id)
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
        print("SKILLS=====>", skills)
        context = {
            'page_title': 'Home',
            'heading': heading,
            'headline': headline,
            'profile_photo': profile_photo,
            'about': about,
            'skills': skills
        }
    except Exception as err:
        print("EXCEPTION=====>", str(err))
        context = {
            'page_title': 'Home',
        }
    return render(request, template, context)


def user_signup(request):
    """
    Registers the user with the system
    """
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
    try:
        pass
    except Exception as err:
        print("EXCEPTION=====>", str(err))
