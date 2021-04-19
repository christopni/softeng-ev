from django.test import TestCase
from rest_framework.test import  APITestCase, APIRequestFactory
from django.urls import reverse, resolve
from datetime import datetime
from django.urls import reverse
import json
from django.db import models
from django.contrib.auth.models import User
from ..views import *
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class TestUsermodView(APITestCase):
    '''
    Only Admin have permissions
    '''
    '''
    Url: evcharge/api/admin/usermod/<str:username>/<str:password>/
    '''

    def setUp(self):
        self.factory = APIRequestFactory()
        self.loginview = LoginView.as_view()
        self.view = UsermodView.as_view()
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.admin = User(username = 'testuser', password = make_password('password'))
        self.admin.save()
        self.admin_group.user_set.add(self.admin)
        request = self.factory.post("/evcharge/api/login/?username=testuser&password=password")
        response = self.loginview(request)
        self.token = response.data['token']


    def test_simple_running(self):
        username = 'testusername'
        password = 'testpassword'
        kwargs = {'username': username, 'password': password}
        url = reverse('usermod', kwargs = kwargs)
        request = self.factory.post(url+'?role=CarOwner&firstname=Test&lastname=TestLast&email=test@mail.com', HTTP_AUTHORIZATION = 'Token ' + self.token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        username = 'testusername2'
        password = 'testpassword2'
        kwargs = {'username': username, 'password': password}
        url = reverse('usermod', kwargs = kwargs)
        request = self.factory.post(url+'?role=CarOwner&firstname=Test&lastname=TestLast&email=test@mail.com', HTTP_AUTHORIZATION = 'Token ' + self.token)
        response = self.view(request, **kwargs)
        self.assertEqual(not auth.authenticate(username = username, password = password), False)


    def test_setup_password(self):
        username = 'testusername2'
        password = 'testpassword2'
        kwargs = {'username': username, 'password': password}
        url = reverse('usermod', kwargs=kwargs)
        request = self.factory.post(url + '?role=CarOwner&firstname=Test&lastname=TestLast&email=test@mail.com',HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.view(request, **kwargs)
        password = 'changepassword'
        kwargs = {'username': username, 'password': password}
        url = reverse('usermod', kwargs = kwargs)
        request = self.factory.post(url+'?role=CarOwner&firstname=Test&lastname=TestLast&email=test@mail.com', HTTP_AUTHORIZATION = 'Token ' + self.token)
        response = self.view(request, **kwargs)
        self.assertEqual(not auth.authenticate(username = username, password = password), False)


    def test_call_as_carowner(self):
        carowner_group, _ = Group.objects.get_or_create(name='CarOwner')
        user = User(username = 'carowner', password = make_password('carowner'))
        user.save()
        carowner_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=carowner&password=carowner")
        response = self.loginview(request)
        self.token = response.data['token']
        username = 'testusername2'
        password = 'testpassword2'
        kwargs = {'username': username, 'password': password}
        url = reverse('usermod', kwargs = kwargs)
        request = self.factory.post(url+'?role=CarOwner&firstname=Test&lastname=TestLast&email=test@mail.com', HTTP_AUTHORIZATION = 'Token ' + self.token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 401)