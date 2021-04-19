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
class TestSessionPerPointView(APITestCase):
    '''
    Admin, EnergyProvider, Municipality and ParkingOwner have permissions
    '''
    '''
    evcharge/api/SessionsPerProvider/<int:provider_id>/<str:start_date>/<str:end_date>/
    '''

    def setUp(self):
        self.factory = APIRequestFactory()
        '''Create Point Operator'''
        self.user_operator = User(username = 'testoperator', password = make_password('testpasswordoperator'))
        self.user_operator.save()
        self.pointoperator = PointOperator.objects.create(user_id = self.user_operator, name = 'TestOperator')
        '''Create Energy Provider'''
        self.user_provider = User(username = 'testprovider', password = make_password('testpasswordprovider'))
        self.user_provider.save()
        self.provider = EnergyProviders.objects.create(id = self.user_provider, slow_charge_cost = 0.5, fast_charge_cost = 1)
        '''Create Station'''
        self.station = LocationofStations.objects.create(point_operator_user_id = self.pointoperator)
        '''Create Point'''
        self.point = Station.objects.create(provider_user_id = self.provider, location_id = self.station)
        '''Create CarOwner'''
        self.user_carowner = User(username = 'testcarowner', password = make_password('testpasswordcarowner'))
        self.user_carowner.save()
        self.carowner = CarOwner.objects.create(user_id = self.user_carowner)
        '''Create Vehicle'''
        self.vehicle = Vehicle.objects.create(carowner = self.carowner)

        '''Create Charge'''
        self.charge = Charge.objects.create(vehicle_carowner_id = self.vehicle, station_id_id = self.point, started_on = datetime(2019, 12, 12), finished_on = datetime(2019, 12, 12),
                                            energy_amount = 30, amount = 25)

        self.loginview = LoginView.as_view()
        self.view = SessionPerProviderView.as_view()
        self.logoutview = LogoutView.as_view()

        '''Create Groups'''
        self.admin_group, _ = Group.objects.get_or_create(name='Admin')
        self.carowner_group, _ = Group.objects.get_or_create(name='CarOwner')
        self.energyproviders_group, _ = Group.objects.get_or_create(name='EnergyProviders')
        self.municipality_group, _ = Group.objects.get_or_create(name='Municipality')
        self.parkingowner_group, _ = Group.objects.get_or_create(name='ParkingOwner')

    def test_call_as_admin(self):
        '''Create User'''
        user = User(username = 'testuser1', password = make_password('testpassword1'))
        user.save()
        self.admin_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=testuser1&password=testpassword1")
        response = self.loginview(request)
        token = response.data['token']
        provider_id = self.provider.id.id
        start_date = '20101010'
        end_date = '20201213'
        kwargs = {'provider_id': provider_id, 'start_date': start_date, 'end_date': end_date}
        url = reverse('session_per_provider', kwargs = kwargs)
        request = self.factory.get(url, HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_call_as_carowner(self):
        user = User(username = 'testuser2', password = make_password('testpassword2'))
        user.save()
        self.carowner_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=testuser2&password=testpassword2")
        response = self.loginview(request)
        token = response.data['token']
        provider_id = self.provider.id.id
        start_date = '20101010'
        end_date = '20201213'
        kwargs = {'provider_id': provider_id, 'start_date': start_date, 'end_date': end_date}
        url = reverse('session_per_provider', kwargs = kwargs)
        request = self.factory.get(url, HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 401)

    def test_call_as_energyproviders(self):
        user = User(username='testuser3', password=make_password('testpassword3'))
        user.save()
        self.energyproviders_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=testuser3&password=testpassword3")
        response = self.loginview(request)
        token = response.data['token']
        provider_id = self.provider.id.id
        start_date = '20101010'
        end_date = '20201213'
        kwargs = {'provider_id': provider_id, 'start_date': start_date, 'end_date': end_date}
        url = reverse('session_per_provider', kwargs=kwargs)
        request = self.factory.get(url, HTTP_AUTHORIZATION='Token ' + token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 200)


    def test_call_as_municipality(self):
        user = User(username = 'testuser4', password = make_password('testpassword4'))
        user.save()
        self.municipality_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=testuser4&password=testpassword4")
        response = self.loginview(request)
        token = response.data['token']
        provider_id = self.provider.id.id
        start_date = '20101010'
        end_date = '20201213'
        kwargs = {'provider_id': provider_id, 'start_date': start_date, 'end_date': end_date}
        url = reverse('session_per_provider', kwargs = kwargs)
        request = self.factory.get(url, HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_call_as_parkingowner(self):
        user = User(username = 'testuser5', password = make_password('testpassword5'))
        user.save()
        self.parkingowner_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=testuser5&password=testpassword5")
        response = self.loginview(request)
        token = response.data['token']
        provider_id = self.provider.id.id
        start_date = '20101010'
        end_date = '20201213'
        kwargs = {'provider_id': provider_id, 'start_date': start_date, 'end_date': end_date}
        url = reverse('session_per_provider', kwargs = kwargs)
        request = self.factory.get(url, HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 200)

    def test_call_with_invalid_provider(self):
        user = User(username = 'testuser6', password = make_password('testpassword6'))
        user.save()
        self.admin_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=testuser6&password=testpassword6")
        response = self.loginview(request)
        token = response.data['token']
        provider_id = self.provider.id.id + 1
        start_date = '20101010'
        end_date = '20201213'
        kwargs = {'provider_id': provider_id, 'start_date': start_date, 'end_date': end_date}
        url = reverse('session_per_provider', kwargs = kwargs)
        request = self.factory.get(url, HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 400)

    def test_call_without_data(self):
        user = User(username = 'testuser7', password = make_password('testpassword7'))
        user.save()
        self.admin_group.user_set.add(user)
        request = self.factory.post("/evcharge/api/login/?username=testuser7&password=testpassword7")
        response = self.loginview(request)
        token = response.data['token']
        provider_id = self.provider.id.id
        start_date = '20221010'
        end_date = '20231213'
        kwargs = {'provider_id': provider_id, 'start_date': start_date, 'end_date': end_date}
        url = reverse('session_per_provider', kwargs = kwargs)
        request = self.factory.get(url, HTTP_AUTHORIZATION = 'Token ' + token)
        response = self.view(request, **kwargs)
        self.assertEqual(response.status_code, 402)

