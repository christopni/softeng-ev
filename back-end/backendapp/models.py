from django.db import models
from django.contrib.auth.models import User

class CarOwner(models.Model):
    user_id = models.OneToOneField(User, null = False, primary_key = True, on_delete = models.CASCADE)
    card_number = models.CharField(unique = True, max_length = 20, null = True)
    phone = models.CharField(max_length = 20, null = True)

class MonthlyCharge(models.Model):
    user_id_id = models.ForeignKey(CarOwner,  null = False, on_delete = models.CASCADE)
    MONTH_CHOICES  = [(str(i), str(i)) for i in range(1, 13)]
    month = models.CharField(max_length = 9, choices = MONTH_CHOICES, default = '1')
    year = models.CharField(max_length = 4)
    total_amount = models.FloatField()
    already_paid = models.SmallIntegerField()

class Vehicle(models.Model):
    carowner = models.OneToOneField(CarOwner, primary_key = True, on_delete = models.CASCADE)
    brand_type = models.CharField(max_length = 100, null = True)
    model = models.CharField(max_length = 100, null = True)
    type = models.CharField(max_length = 100, null = True)
    release_year = models.CharField(max_length = 4, null = True)
    usable_battery_size = models.FloatField(null = True)
    km_after_prev_charge = models.FloatField(null = True)

class PointOperator(models.Model):
    user_id = models.OneToOneField(User, null = False, primary_key = True, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, null = True)

class Area(models.Model):
    user_id = models.OneToOneField(User, null=False, primary_key = True, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100, null = True)

class LocationofStations(models.Model):
    point_operator_user_id = models.ForeignKey(PointOperator, null = True, on_delete = models.CASCADE)
    area_user_id = models.ForeignKey(Area, null = True, on_delete = models.CASCADE)
    address = models.CharField(max_length = 100, null = True)
    address_postal_code = models.CharField(max_length = 100, null = True)
    latitude = models.FloatField(null = True)
    longitude = models.FloatField(null = True)
    address_region = models.CharField(max_length = 100, null = True)
    phone = models.CharField(max_length = 20, null = True)
    private = models.SmallIntegerField(null = True)
    open_hour = models.TimeField(null = True)
    close_hour = models.TimeField(null = True)

class EnergyProviders(models.Model):
    id = models.OneToOneField(User, null = False, primary_key = True, on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, null = True)
    fast_charge_cost = models.FloatField(null = True)
    slow_charge_cost = models.FloatField(null = True)

class Station(models.Model):
    provider_user_id = models.ForeignKey(EnergyProviders, on_delete = models.CASCADE)
    location_id = models.ForeignKey(LocationofStations, on_delete = models.CASCADE)
    available = models.SmallIntegerField(null = True)
    expected_time = models.IntegerField(null = True)

class Charge(models.Model):
    vehicle_carowner_id = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    station_id_id = models.ForeignKey(Station, on_delete = models.CASCADE)
    started_on = models.DateTimeField(null = True)
    finished_on = models.DateTimeField(null = True)
    energy_amount = models.FloatField(null = True)
    amount = models.FloatField(null = True)
    PAYMENT_CHOICES = [(str(1), 'cash'), (str(2), 'card'), (str(3), 'month bill')]
    payment_method = models.CharField(max_length = 10, choices = PAYMENT_CHOICES, default = '1', null = True)
    PROTOCOL_CHOICES = [(str(1), 'slow'), (str(2), 'fast')]
    protocol = models.CharField(max_length = 4, choices = PROTOCOL_CHOICES, default = '1', null = True)

class StationRating(models.Model):
    carowner_id = models.ForeignKey(User, on_delete = models.CASCADE)
    station_id = models.ForeignKey(Station, on_delete = models.CASCADE)
    RATING_CHOICES = [(str(i), i) for i in range(1, 6)]
    rating = models.IntegerField(choices = RATING_CHOICES, default = '1', null = True)

class ApiKey(models.Model):
    apikey = models.CharField(max_length = 100, primary_key = True)