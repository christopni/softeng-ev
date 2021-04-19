from rest_framework import serializers
from django.db.models import Sum
from .models import *
from django.contrib.auth.models import *
from datetime import datetime

class EnergyProviderSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = EnergyProviders
		fields = ('id_id','name','fast_charge_cost','slow_charge_cost')

class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):    
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ['groups']

class SessionsPerPoint_ChargeSerializer(serializers.BaseSerializer):

    def to_representation(self, instance):
        self.context['serial_number'] = self.context['serial_number'] + 1
        return {
            'SessionIndex': self.context['serial_number'],
            'SessionID' : str(instance.id),
            'StartedOn' : instance.started_on.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'FinishedOn' : instance.finished_on.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'Protocol' : instance.protocol,
            'EnergyDelivered' : round(instance.energy_amount, 2),
            'Payment' : instance.payment_method,
            'VehicleType' : Vehicle.objects.get(charge__pk = instance.id).type
        }


class SessionsPerStation_PointSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        startdate = self.context['startdate']
        enddate = self.context['enddate']
        return {
            'PointID' : str(instance.id),
            'PointSessions' : Charge.objects.filter(station_id_id = instance.id,
                                                  finished_on__range = [startdate,  enddate],
                                                  started_on__range = [startdate,  enddate]).count(),
            'EnergyDelivered' : round(Station.objects.filter(pk = instance.id, charge__finished_on__range=[startdate, enddate],
                                                           charge__started_on__range=[startdate, enddate]).annotate(total_sum = Sum('charge__energy_amount')).first().total_sum, 2)
        }


class SessionsPerEV_ChargeSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):

        if instance.protocol == 'fast':
            cost = EnergyProviders.objects.get(station__charge__pk = instance.id).fast_charge_cost
        else:
            cost = EnergyProviders.objects.get(station__charge__pk=instance.id).slow_charge_cost

        self.context['serial_number'] = self.context['serial_number'] + 1
        return {
            'SessionIndex' : self.context['serial_number'],
            'SessionID' : str(instance.id),
            'EnergyProvider' : EnergyProviders.objects.get(station__charge__pk = instance.id).name,
            'StartedOn' : instance.started_on.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'FinishedOn' : instance.finished_on.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'EnergyDelivered' : round(instance.energy_amount, 2),
            'PricePolicyRef' : instance.protocol,
            'CostPerKWh' : round(cost, 2),
            'SessionCost' : round(instance.amount, 2)
        }


class SessionsPerProvider_ChargeSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):

        if instance.protocol == 'fast':
            cost = EnergyProviders.objects.get(station__charge__pk = instance.id).fast_charge_cost
        else:
            cost = EnergyProviders.objects.get(station__charge__pk=instance.id).slow_charge_cost
        return {
            'StationID' : str(self.context[instance.id]),
            'SessionID' : instance.id,
            'VehicleID' : str(instance.vehicle_carowner_id.carowner.user_id.id),
            'StartedOn' : instance.started_on.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'FinishedOn' : instance.finished_on.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'EnergyDelivered' : round(instance.energy_amount, 2),
            'PricePolicyRef' : instance.protocol,
            'CostPerKWh' : round(cost, 2),
            'TotalCost' : round(instance.amount, 2)
        }


class SessionsPerProvider_StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'location_id', 'charge_set']


class ProviderStatistics_StationSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'StationID': instance.id,
            'Address': LocationofStations.objects.get(id=instance.location_id.id).address,
            'AddressRegion': LocationofStations.objects.get(id=instance.location_id.id).address_region,
            'LocationID': instance.location_id.id
        }


class OperatorStatistics_LocationsSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'LocationID': instance.id,
            'Address': instance.address,
            'AddressRegion': instance.address_region
        }


class OperatorLocationDetails_LocationSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'LocationID' : instance.id,
            'Address' : instance.address,
            'AddressPostalCode' : instance.address_postal_code,
            'AddressRegion' : instance.address_region,
            'Phone' : instance.phone,
            'OpenHours' : instance.open_hour,
            'CloseHours' : instance.close_hour
        }

class OperatorEnergyProvidersDetails_ProvidersSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'ID' : instance.id.id,
            'Name' : instance.name,
            'FastChargeCost' : instance.fast_charge_cost,
            'LowChargeCost' : instance.slow_charge_cost
        }


class RightLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationofStations
        fields = '__all__'


class AllLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationofStations
        fields = ['address_region']


class MonthlyChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyCharge
        fields = ['id', 'month','year','total_amount']


class SpecificPointsSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'PointID' : instance.id,
            'Fast_Charge_Cost' : EnergyProviders.objects.get(station__id = instance.id).fast_charge_cost,
            'Slow_Charge_Cost' : EnergyProviders.objects.get(station__id = instance.id).slow_charge_cost
        }


class LocationPointsSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'PointID' : instance.id,
            'ProviderName' : EnergyProviders.objects.get(station__id = instance.id).name
            }



class SendAllLocationsSerializer(serializers.BaseSerializer):
    class Meta:
        model = LocationofStations
        fields = '_all_'