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
from .views import *
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

class UsersTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        
    def test_create_user(self):
        #user = User.objects.get(username = 'testuser')      
        self.assertEqual(not User.objects.get(username = 'testuser'), False)
        
        

class CarOwnerTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        group, created = Group.objects.get_or_create(name='CarOwner')
        group = Group.objects.get(name='CarOwner')
        group.user_set.add(self.user)
        self.carowner = CarOwner.objects.create(user_id = self.user)
        
    def test_create_carowner(self):
        self.assertEqual(not CarOwner.objects.get(user_id = self.user.id), False)
        
        
class PointOperatorTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        group, created = Group.objects.get_or_create(name='ParkingOwner')
        group = Group.objects.get(name='ParkingOwner')
        group.user_set.add(self.user)
        self.pointoperator = PointOperator.objects.create(user_id = self.user)
        
    def test_create_pointoperator(self):
        self.assertEqual(not PointOperator.objects.get(user_id = self.user.id), False)
        
        
class AreaTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        group, created = Group.objects.get_or_create(name='Municipality')
        group = Group.objects.get(name='Municipality')
        group.user_set.add(self.user)
        self.area = Area.objects.create(user_id = self.user)
        
    def test_create_area(self):
        self.assertEqual(not Area.objects.get(user_id = self.user.id), False)
        
        
class EnergyProvidersTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        group, created = Group.objects.get_or_create(name='EnergyProviders')
        group = Group.objects.get(name='EnergyProviders')
        group.user_set.add(self.user)
        self.energyproviders = EnergyProviders.objects.create(id = self.user, name = 'AAA', fast_charge_cost = 1, slow_charge_cost = 0.5)
        
    def test_create_energyproviders(self):
        self.assertEqual(not EnergyProviders.objects.get(id = self.user.id), False)
        
    def test_create_energyproviders_name(self):
        self.assertEqual(not EnergyProviders.objects.get(id = self.user.id).name, False)
        
    def test_create_energyproviders_fast_charge_cost(self):
        self.assertEqual(not EnergyProviders.objects.get(id = self.user.id).fast_charge_cost, False)
        
    def test_create_energyproviders_slow_charge_cost(self):
        self.assertEqual(not EnergyProviders.objects.get(id = self.user.id).slow_charge_cost, False)
        
class VehicleTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        self.carowner = CarOwner.objects.create(user_id = self.user)
        self.vehicle = Vehicle.objects.create(pk = self.user.id, carowner = self.carowner, usable_battery_size = 10, km_after_prev_charge = 20)
        
    def test_create_vehicle(self):
        self.assertEqual(not Vehicle.objects.get(pk = self.user.id), False)
        
    def test_create_vehicle_carowner(self):
        self.assertEqual(not Vehicle.objects.get(pk = self.user.id).carowner, False)
        
    def test_create_vehicle_usable_battery_size(self):
        self.assertEqual(not Vehicle.objects.get(pk = self.user.id).usable_battery_size, False)
        
    def test_create_vehicle_km_after_prev_charge(self):
        self.assertEqual(not Vehicle.objects.get(pk = self.user.id).km_after_prev_charge, False)
        
    
class LocationOfStationsTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        group, created = Group.objects.get_or_create(name='ParkingOwner')
        group = Group.objects.get(name='ParkingOwner')
        group.user_set.add(self.user)
        self.pointoperator = PointOperator.objects.create(user_id = self.user)
        self.locationofstations = LocationofStations.objects.create(pk = self.user.id, point_operator_user_id = self.pointoperator, address = 'AA', address_postal_code = '2344', latitude = 15, longitude = 78, address_region = 'agvh', private = 1, open_hour = '05:05:00', close_hour = '21:00:00')
        
    def test_create_locationofstations(self):
        self.assertEqual(not LocationofStations.objects.get(pk = self.user.id), False)
        
    def test_create_locationofstations_point_operator(self):
        self.assertEqual(not LocationofStations.objects.get(pk = self.user.id).point_operator_user_id, False)
     
class StationTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        self.pointoperator = PointOperator.objects.create(user_id = self.user)
        self.locationofstations = LocationofStations.objects.create(pk = self.user.id, point_operator_user_id = self.pointoperator, address = 'AA', address_postal_code = '2344', latitude = 15, longitude = 78, address_region = 'agvh', private = 1, open_hour = '05:05:00', close_hour = '21:00:00')
        self.energyproviders = EnergyProviders.objects.create(id = self.user, name = 'AAA', fast_charge_cost = 1, slow_charge_cost = 0.5)
        self.station = Station.objects.create(pk = self.user.id, provider_user_id = self.energyproviders, location_id = self.locationofstations, available = 1, expected_time = 0)
        
    def test_create_station(self):
        self.assertEqual(not Station.objects.get(pk = self.user.id), False)
        
    def test_create_station_provider_user_id(self):
        self.assertEqual(not Station.objects.get(pk = self.user.id).provider_user_id, False)
        
    def test_create_station_location_id(self):
        self.assertEqual(not Station.objects.get(pk = self.user.id).location_id, False)
        
   
class ChargeTestCase(TestCase):
    def setUp(self):
        self.user =  User(username = 'testuser', password = make_password('testpassword'))
        self.user.save()
        self.carowner = CarOwner.objects.create(user_id = self.user)
        self.vehicle = Vehicle.objects.create(pk = self.user.id, carowner = self.carowner, usable_battery_size = 10, km_after_prev_charge = 20)
        self.pointoperator = PointOperator.objects.create(user_id = self.user)
        self.locationofstations = LocationofStations.objects.create(pk = self.user.id, point_operator_user_id = self.pointoperator, address = 'AA', address_postal_code = '2344', latitude = 15, longitude = 78, address_region = 'agvh', private = 1, open_hour = '05:05:00', close_hour = '21:00:00')
        self.energyproviders = EnergyProviders.objects.create(id = self.user, name = 'AAA', fast_charge_cost = 1, slow_charge_cost = 0.5)
        self.station = Station.objects.create(pk = self.user.id, provider_user_id = self.energyproviders, location_id = self.locationofstations, available = 1, expected_time = 0)
        self.charge = Charge.objects.create(pk = self.user.id, vehicle_carowner_id = self.vehicle, station_id_id = self.station, started_on = "2018-04-25 11:08:04.000000", finished_on = "2018-04-25 11:08:04.000000", energy_amount = 100, amount = 100, payment_method = "cash", protocol = "fast")
        
    def test_create_charge(self):
        self.assertEqual(not Station.objects.get(pk = self.user.id), False)
        
    def test_create_charge_vehicle_carowner_id(self):
        self.assertEqual(not Charge.objects.get(pk = self.user.id).vehicle_carowner_id, False)
        
    def test_create_charge_station_id_id(self):
        self.assertEqual(not Charge.objects.get(pk = self.user.id).station_id_id, False)
       
  