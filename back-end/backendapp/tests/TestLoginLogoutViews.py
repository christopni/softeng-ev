from django.test import TestCase
from rest_framework.test import  APITestCase, APIRequestFactory
from django.urls import reverse, resolve
from datetime import datetime
#from django.views import LoginView
from django.urls import reverse
#from rest_framework.test import APIRequestFactory
#rom rest_framework.test import TestCase
#from myproject.apps.core.models import Account
import json
from django.db import models
from django.contrib.auth.models import User
from ..views import *
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class TestLoginView(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        self.loginview = LoginView.as_view()
        group, created = Group.objects.get_or_create(name='EnergyProviders')
        group = Group.objects.get(name='EnergyProviders')
        group.user_set.add(self.user)

    def test_login(self):
        request = self.factory.post("/evcharge/api/login/?username=testuser&password=testpassword")
        response = self.loginview(request)
        self.assertEqual(response.status_code, 200)

    def test_login_with_no_data(self):
        request = self.factory.post("/evcharge/api/login/")
        response = self.loginview(request)
        self.assertEqual(response.status_code, 400)

    def test_login_with_invalid_data(self):
        request = self.factory.post("/evcharge/api/login/?username=testuser&password=password")
        response = self.loginview(request)
        self.assertEqual(response.status_code, 401)

class TestLogoutView(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        self.user.groups.add(2)
        self.loginview = LoginView.as_view()
        self.logoutview = LogoutView.as_view()
        group, created = Group.objects.get_or_create(name='EnergyProviders')
        group = Group.objects.get(name='EnergyProviders')
        group.user_set.add(self.user)

    def test_logout(self):
        request = self.factory.post("/evcharge/api/login/?username=testuser&password=testpassword")
        response = self.loginview(request)
        token = response.data['token']
        request = self.factory.post("/evcharge/api/logout/", HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.logoutview(request)
        self.assertEqual(response.status_code, 200)

    def test_logout_without_token(self):
        request = self.factory.post("/evcharge/api/login/?username=testuser&password=testpassword")
        response = self.loginview(request)
        token = response.data['token']
        request = self.factory.post("/evcharge/api/logout/")
        response = self.logoutview(request)
        self.assertEqual(response.status_code, 400)

    def test_logout_without_login(self):
        token = "tokentokentokentokentokentokentoken"
        request = self.factory.post("/evcharge/api/logout/", HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.logoutview(request)
        self.assertEqual(response.status_code, 401)
