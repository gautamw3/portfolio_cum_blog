"""
Contains the classes which wraps the function to return global
objects in case no user is logged in and default details need
to be rendered in order to serve

Created on: Jan, 29th 2023
Created by: Gautam Kumar
"""


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
        self.pk = 8
        self.user_model = user_model
        self.user_obj = None

    def get_user_obj(self):
        self.user_obj = self.user_model.objects.get(pk=8)
        return self.user_obj
