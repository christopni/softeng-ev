from django.shortcuts import render
from django.conf import settings
from django.contrib import auth
from datetime import datetime
from geopy.geocoders import Nominatim
from django.contrib.auth.hashers import make_password
from django.db.models import Sum, Count
from rest_framework_csv.renderers import JSONRenderer, CSVRenderer
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import *
from .models import *
import csv, codecs

class LoginView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def post(self, request):
        data = request.GET
        try:
            username = data['username']
            password = data['password']
        except:
            return Response({'Not enough parameters'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        user = auth.authenticate(username = username, password = password)
        if user:
            auth_token = str(Token.objects.create(user = user))
            group = list(user.groups.values_list('name', flat = True))[0]
            data = {'user': group, 'token':auth_token}
            return Response(data, status = status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def post(self, request, format = None):
        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)


        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)


class SessionPerPointView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):
        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        group = list(user.groups.values_list('name', flat=True))[0]
        if group == 'CarOwner':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            point_id = kwargs['point_id']
            start_date = kwargs['start_date']
            end_date = kwargs['end_date']
        except:
            return Response({'Not enough parameters'}, status=status.HTTP_400_BAD_REQUEST)

        startdate = str(start_date[:4] + '-' + start_date[4:6] + '-' + start_date[6:])
        enddate = str(end_date[:4] + '-' + end_date[4:6] + '-' + end_date[6:])

        json = dict()
        json['Point'] = str(point_id)

        try:
            c = Station.objects.get(pk = point_id)
        except:
            return Response({'Invalid PointID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            json['PointOperator'] = PointOperator.objects.get(locationofstations__station__id = point_id).name
        except:
            json['PointOperator'] = Area.objects.get(locationofstations__station__id = point_id).name


        d = datetime.now()
        json['RequestTimestamp'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = datetime(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
        json['PeriodFrom'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = datetime(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:]))
        json['PeriodTo'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")

        charges_queryset = Charge.objects.filter(station_id_id = point_id,
                                                  finished_on__range = [startdate,  enddate],
                                                  started_on__range = [startdate,  enddate])

        if not charges_queryset:
            json['NumberOfChargingSessions'] = 0
            json['ChargingSessionsList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['NumberOfChargingSessions'] = charges_queryset.count()
        sessions_serializer = SessionsPerPoint_ChargeSerializer(charges_queryset, many=True,
                                                                context={'serial_number': 0})
        json['ChargingSessionsList'] = sessions_serializer.data

        json_file = []
        json_file.append(json)

        return Response(json, status = status.HTTP_200_OK)


class SessionPerStationView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        group = list(user.groups.values_list('name', flat=True))[0]
        if group == 'CarOwner':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            station_id = kwargs['station_id']
            start_date = kwargs['start_date']
            end_date = kwargs['end_date']
        except:
            return Response({'Not enough parameters'}, status=status.HTTP_400_BAD_REQUEST)

        startdate = str(start_date[:4] + '-' + start_date[4:6] + '-' + start_date[6:])
        enddate = str(end_date[:4] + '-' + end_date[4:6] + '-' + end_date[6:])

        json = dict()
        json['StationID'] = str(station_id)

        try:
            c = LocationofStations.objects.get(pk = station_id)
        except:
            return Response({'Invalid StationID'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            json['Operator'] = PointOperator.objects.get(locationofstations__pk = station_id).name
        except:
            json['Operator'] = Area.objects.get(locationofstations__pk = station_id).name

        d = datetime.now()
        json['RequestTimestamp'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = datetime(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
        json['PeriodFrom'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = datetime(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:]))
        json['PeriodTo'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")

        station_queryset = Station.objects.filter(location_id = station_id,
                                            charge__finished_on__range = [startdate,  enddate],
                                            charge__started_on__range = [startdate,  enddate]).annotate(total_price=Sum('charge__energy_amount'))

        if not station_queryset:
            json['TotalEnergyDelivered'] = 0
            json['NumberOfChargingSessions'] = 0
            json['NumberOfActivePoints'] = 0
            json['SessionsSummaryList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['TotalEnergyDelivered'] = round(LocationofStations.objects.filter(id = station_id,
                                                                        station__charge__finished_on__range = [startdate, enddate],
                                                                        station__charge__started_on__range = [startdate, enddate]).annotate(total_price = Sum('station__charge__energy_amount')).first().total_price, 2)

        json['NumberOfChargingSessions'] = LocationofStations.objects.filter(id = station_id,
                                                                        station__charge__finished_on__range = [startdate, enddate],
                                                                        station__charge__started_on__range = [startdate, enddate]).annotate(total_count = Count('station__charge__pk')).first().total_count
        json['NumberOfActivePoints'] = LocationofStations.objects.filter(id = station_id,
                                                                        station__charge__finished_on__range = [startdate, enddate],
                                                                        station__charge__started_on__range = [startdate, enddate]).annotate(total_count = Count('station__pk', distinct = True)).first().total_count

        points_queryset = Station.objects.filter(location_id = station_id,
                                            charge__finished_on__range = [startdate,  enddate],
                                            charge__started_on__range = [startdate,  enddate]).all().distinct()

        if not points_queryset:
            json['TotalEnergyDelivered'] = 0
            json['NumberOfChargingSessions'] = 0
            json['NumberOfActivePoints'] = 0
            json['SessionsSummaryList'] = []
            return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)

        json['SessionsSummaryList'] = SessionsPerStation_PointSerializer(points_queryset, context = {'startdate' : startdate, 'enddate' : enddate}, many = True ).data

        json_file = []
        json_file.append(json)

        return Response(json, status = status.HTTP_200_OK)


class SessionPerEVView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        group = list(user.groups.values_list('name', flat=True))[0]
        if group == 'CarOwner':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            vehicle_id = kwargs['vehicle_id']
            start_date = kwargs['start_date']
            end_date = kwargs['end_date']
        except:
            return Response({'Not enough parameters'}, status = status.HTTP_400_BAD_REQUEST)

        startdate = str(start_date[:4] + '-' + start_date[4:6] + '-' + start_date[6:])
        enddate = str(end_date[:4] + '-' + end_date[4:6] + '-' + end_date[6:])

        json = dict()
        json['VehicleID'] = str(vehicle_id)

        try:
            c = Vehicle.objects.get(carowner = vehicle_id)
        except:
            return Response({'Invalid VehicleID'}, status=status.HTTP_400_BAD_REQUEST)

        d = datetime.now()
        json['RequestTimestamp'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = datetime(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
        json['PeriodFrom'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        d = datetime(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:]))
        json['PeriodTo'] = d.strftime("%Y-%m-%d %H:%M:%S.%f")

        vehicle_queryset = Vehicle.objects.filter(carowner = vehicle_id,
                                     charge__started_on__range = [startdate, enddate],
                                     charge__finished_on__range = [startdate, enddate]).annotate(total_price = Sum('charge__energy_amount'), total_count = Count('charge__station_id_id', distinct = True)).first()

        if not vehicle_queryset:
            json['TotalEnergyConsumed'] = 0
            json['NumberOfVisitedPoints'] = 0
            json['NumberOfVehicleChargingSessions'] = 0
            json['VehicleChargingSessionsList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['TotalEnergyConsumed'] = round(vehicle_queryset.total_price, 2)
        json['NumberOfVisitedPoints'] = round(vehicle_queryset.total_count, 2)

        charges_queryset = Charge.objects.filter(vehicle_carowner_id = vehicle_id,
                                                finished_on__range=[startdate, enddate],
                                                started_on__range=[startdate, enddate])
        if not charges_queryset:
            json['TotalEnergyConsumed'] = 0
            json['NumberOfVisitedPoints'] = 0
            json['NumberOfVehicleChargingSessions'] = 0
            json['VehicleChargingSessionsList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['NumberOfVehicleChargingSessions'] = charges_queryset.count()

        json['VehicleChargingSessionsList'] = SessionsPerEV_ChargeSerializer(charges_queryset, many = True, context = {'serial_number' : 0}).data

        json_file = []
        json_file.append(json)

        return Response(json, status=status.HTTP_200_OK)

from django.db import connection

class SessionPerProviderView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        group = list(user.groups.values_list('name', flat=True))[0]
        if group == 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            provider_id = kwargs['provider_id']
            start_date = kwargs['start_date']
            end_date = kwargs['end_date']
        except:
            return Response({'Not enough parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            c = EnergyProviders.objects.get(id = provider_id)
        except:
            return Response({'Invalid ProviderID'}, status = status.HTTP_400_BAD_REQUEST)

        startdate = str(start_date[:4] + '-' + start_date[4:6] + '-' + start_date[6:])
        enddate = str(end_date[:4] + '-' + end_date[4:6] + '-' + end_date[6:])

        json = dict()
        json['ProviderID'] = str(provider_id)
        json['ProviderName'] = EnergyProviders.objects.get(id = provider_id).name

        station_queryset = Station.objects.filter(provider_user_id = provider_id,
                                                  charge__finished_on__range=[startdate, enddate],
                                                  charge__started_on__range=[startdate, enddate]).all()
        if not station_queryset:
            json['ProviderChargingSessionsList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        station_serializer_data = list(SessionsPerProvider_StationSerializer(station_queryset, many = True).data)

        charges_pks = []
        context_charges_pks = dict()
        for p in station_serializer_data:
            for c in p['charge_set']:
                charges_pks.append(c)
                context_charges_pks[c] = p['location_id']

        charges_queryset = Charge.objects.filter(pk__in = charges_pks).all()

        json['NumberOfProviderChargingSessions'] = charges_queryset.count()


        if not charges_queryset:
            json['NumberOfProviderChargingSessions'] = 0
            json['ProviderChargingSessionsList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['ProviderChargingSessionsList'] = SessionsPerProvider_ChargeSerializer(charges_queryset, many = True, context = context_charges_pks).data
        return Response(json, status=status.HTTP_200_OK)



class HealthcheckView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):
        data = {}

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk = apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        try:
            q = User.objects.all()
        except:
            data["status"] = "failed"
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data["status"] = "OK"
        return Response(data, status=status.HTTP_200_OK)


class UserElementsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            admin = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        group = list(admin.groups.values_list('name', flat=True))[0]
        if group != 'Admin':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            username = kwargs['username']
        except:
            return Response({'Not enough parameters'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username = username)
        except:
            return Response({'No data'}, status = status.HTTP_402_PAYMENT_REQUIRED)

        json = dict()
        json['ID'] = user.id
        json['Username'] = user.username
        json['FirstName'] = user.first_name
        json['LastName'] = user.last_name
        json['Email'] = user.email
        json['Role'] = list(user.groups.values_list('name', flat=True))[0]
        json['DateJoined'] = user.date_joined.strftime("%Y-%m-%d %H:%M:%S.%f")
        json['LastLogin'] = user.last_login

        return Response(json, status = status.HTTP_200_OK)


class UsermodView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def post(self, request, *args, **kwargs):
        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            apikey = request.GET["apikey"]
            try:
                apikey_exists = ApiKey.objects.get(pk=apikey)
            except:
                return Response({'Not Authorized: Invalid API key' }, status=status.HTTP_401_UNAUTHORIZED)
        except:
            pass

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'Admin':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            username = kwargs['username']
            passw = kwargs['password']
            data = request.GET
            role = data["role"]
            name = data["firstname"]
            surname = data["lastname"]
            mail = data["email"]
        except:
            return Response({"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username__exact = username)
            user.set_password(passw)
            user.save()
            return Response({"status": "OK"}, status = status.HTTP_200_OK)
        except:
            user = User(username = username, password = make_password(passw), email = mail, first_name = name, last_name = surname)
            user.save()
            if (role == 'Admin'):
                user.groups.add(1)
            elif (role == 'CarOwner'):
                user.groups.add(2)
                c = CarOwner.objects.create(user_id = user)
            elif (role == 'EnergyProvider'):
                user.groups.add(3)
                c = EnergyProviders.objects.create(id = user)
            elif (role == 'Municipality'):
                user.groups.add(4)
                c = Area.objects.create(user_id = user)
            elif (role == 'ParkingOwner'):
                user.groups.add(5)
                c = PointOperator.objects.create(user_id = user)
            return Response({"status": "OK"}, status = status.HTTP_200_OK)


class SessionsUpdView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    def post(self, request, *args, **kwargs):
        jsonreply = {}
        try:
            csvReader = csv.DictReader(codecs.iterdecode(request.FILES['file'], 'utf-8'))
            rows_counter = 0
            imported_counter = 0
            for rows in csvReader:
                rows_counter = rows_counter + 1
                vehicle = Vehicle.objects.get(carowner = rows['vehicle_carowner_id_id'] )
                station = Station.objects.get(pk = rows['station_id_id_id'])
                start_date = datetime.strptime(rows['started_on'], "%Y-%m-%d %H:%M:%S")
                end_date = datetime.strptime(rows['finished_on'], "%Y-%m-%d %H:%M:%S")
                charge_already_exists = Charge.objects.filter(finished_on__range=[start_date, end_date],started_on__range=[start_date, end_date],vehicle_carowner_id = rows['vehicle_carowner_id_id'],station_id_id = rows['station_id_id_id'] ).first()
                if not(charge_already_exists):
                    newcharge = Charge(vehicle_carowner_id = vehicle, station_id_id = station, started_on = start_date, finished_on = end_date, energy_amount = rows['energy_amount'],amount = rows['amount'],payment_method = rows['payment_method'] ,protocol = rows['protocol'] )
                    newcharge.save()
                    imported_counter = imported_counter + 1
            jsonreply["SessionsInUploadedFile"] = rows_counter
            jsonreply["SessionsImported"] = imported_counter
            total_sessions = Charge.objects.all().count()
            jsonreply["TotalSessionsInDatabase"] = total_sessions
            return Response(jsonreply,status = status.HTTP_200_OK)
        except:
            return Response({'failed'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProviderStatisticsView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'EnergyProviders':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        json = dict()
        json['EnergyProviderID'] = user.id
        stations_queryset = Station.objects.filter(provider_user_id=json['EnergyProviderID'])

        json['StationsList'] = ProviderStatistics_StationSerializer(stations_queryset, many=True).data
        return Response(json, status=status.HTTP_200_OK)


class OperatorStatisticsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        json = dict()
        json['OperatorID'] = user.id
        if group == 'Municipality':
            json['OperatorName'] = Area.objects.get(pk=json['OperatorID']).name
            locations_queryset = LocationofStations.objects.filter(area_user_id=json['OperatorID'])
        else:
            json['OperatorName'] = PointOperator.objects.get(pk=json['OperatorID']).name
            locations_queryset = LocationofStations.objects.filter(point_operator_user_id=json['OperatorID'])

        if not locations_queryset:
            json['LocationsList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['LocationsList'] = OperatorStatistics_LocationsSerializer(locations_queryset, many=True).data
        return Response(json, status=status.HTTP_200_OK)

class OperatorLocationInsertView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        try:
            data = request.GET
            address = data['address']
            addresspostalcode = data['addresspostalcode']
            addressregion = data['addressregion']
            phone = data['phone']
            openhours = data['openhour']
            closehours = data['closehour']
        except:
            return Response({"Not enough parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            c = LocationofStations.objects.get(address = address, address_postal_code = addresspostalcode, address_region = addressregion)
            return Response({"Location in same address"}, status=status.HTTP_400_BAD_REQUEST)
        except:

            try:
                geolocator = Nominatim(user_agent = "softeng_api")
                location = geolocator.geocode(address)
            except:
                return Response({"Invalid Address"}, status=status.HTTP_400_BAD_REQUEST)

            if group != 'Municipality':
                c = LocationofStations.objects.create(point_operator_user_id = PointOperator.objects.get(pk = user.id), address = address,
                                                      address_postal_code = addresspostalcode, address_region = addressregion,
                                                      phone = phone, private = 1, latitude = location.latitude, longitude = location.longitude,
                                                      open_hour = openhours, close_hour  = closehours)
            else:
                c = LocationofStations.objects.create(area_user_id = Area.objects.get(pk = user.id), address = address,
                                                      address_postal_code = addresspostalcode, address_region = addressregion,
                                                      phone = phone, private = 0, latitude = location.latitude, longitude = location.longitude,
                                                      open_hour = openhours, close_hour  = closehours)

            return Response(status = status.HTTP_200_OK)



class OperatorStationInsertView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)
        try:
            data = request.GET
            locationid = data['locationid']
            providerid = data['providerid']
        except:
            return Response({"Not enough parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = LocationofStations.objects.get(pk = locationid)
        except:
            return Response({"Invalid LocationID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            provider = EnergyProviders.objects.get(pk = providerid)
        except:
            return Response({"Invalid ProviderID"}, status=status.HTTP_400_BAD_REQUEST)


        if group == 'Municipality':
            if location.area_user_id.pk != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)

        else:
            if location.point_operator_user_id.pk != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)

        c = Station.objects.create(provider_user_id = provider,
                                    location_id = location,
                                    available = 0, expected_time = 0)

        return Response(status = status.HTTP_200_OK)


class OperatorLocationDetailsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        json = dict()
        if group == 'Municipality':
            locations_queryset = LocationofStations.objects.filter(area_user_id=user.id)
        else:
            locations_queryset = LocationofStations.objects.filter(point_operator_user_id=user.id)

        if not locations_queryset:
            json['LocationsList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['LocationsList'] = OperatorLocationDetails_LocationSerializer(locations_queryset, many=True).data
        return Response(json, status=status.HTTP_200_OK)


class OperatorEnergyProvidersDetailsView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        json = dict()
        providers_querset = EnergyProviders.objects.filter()

        if not providers_querset:
            json['ProvidersList'] = []
            return Response(json, status = status.HTTP_402_PAYMENT_REQUIRED)

        json['ProvidersList'] = OperatorEnergyProvidersDetails_ProvidersSerializer(providers_querset, many = True).data
        return Response(json, status=status.HTTP_200_OK)


class OperatorLocationUpdatetView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        data = request.GET
        try:
            locationid = data['locationid']
        except:
            return Response({"Not enough parameters"}, status = status.HTTP_400_BAD_REQUEST)

        try:
            location = LocationofStations.objects.get(pk = locationid)
        except:
            return Response({"Invalid LocationID"}, status = status.HTTP_400_BAD_REQUEST)


        if group == 'Municipality':
            if location.area_user_id.pk != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)

        else:
            if location.point_operator_user_id.pk != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)

        try:
            phone = data['phone']
        except:
            phone = 'null'
        try:
            openhours = data['openhour']
        except:
            openhours = 'null'
        try:
            closehours = data['closehour']
        except:
            closehours = 'null'


        if phone == 'null' and openhours == 'null' and closehours == 'null':
            return Response({"None parameter for update"}, status=status.HTTP_400_BAD_REQUEST)


        if phone != 'null':
            LocationofStations.objects.filter(pk = locationid).update(phone = phone)
        if openhours != 'null':
            LocationofStations.objects.filter(pk = locationid).update(open_hour = openhours)
        if closehours != 'null':
            LocationofStations.objects.filter(pk = locationid).update(close_hour = closehours)

        return Response(status = status.HTTP_200_OK)


class OperatorStationUpdatetView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        data = request.GET
        try:
            stationid = data['stationid']
        except:
            return Response({"Not enough parameters"}, status = status.HTTP_400_BAD_REQUEST)

        try:
            station = Station.objects.get(id = stationid)
        except:
            return Response({"Invalid StationID"}, status=status.HTTP_400_BAD_REQUEST)

        if group == 'Municipality':

            areaid = LocationofStations.objects.get(station__id = stationid).area_user_id.pk
            if areaid != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)

        else:
            pointoperatorid = LocationofStations.objects.get(station__id = stationid).point_operator_user_id.pk
            if pointoperatorid != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)

        try:
            providerid = data['providerid']
        except:
            return Response({"None parameter for update"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            provider = EnergyProviders.objects.get(pk = providerid)
        except:
            return Response({"Invalid ProviderID"}, status=status.HTTP_400_BAD_REQUEST)

        Station.objects.filter(pk = stationid).update(provider_user_id = providerid)

        return Response(status = status.HTTP_200_OK)


class OperatorStationDeleteView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status = status.HTTP_401_UNAUTHORIZED)

        data = request.GET
        try:
            stationid = data['stationid']
        except:
            return Response({"Not enough parameters"}, status = status.HTTP_400_BAD_REQUEST)

        try:
            station = Station.objects.get(id = stationid)
        except:
            return Response({"Invalid StationID"}, status=status.HTTP_400_BAD_REQUEST)

        if group == 'Municipality':
            areaid = LocationofStations.objects.get(station__id = stationid).area_user_id.pk
            if areaid != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)
        else:
            pointoperatorid = LocationofStations.objects.get(station__id = stationid).point_operator_user_id.pk
            if pointoperatorid != user.id:
                return Response({"Location not Authorized"}, status = status.HTTP_400_BAD_REQUEST)

        Station.objects.filter(pk = stationid).delete()

        return Response(status = status.HTTP_200_OK)

class ResetSessionView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]
    def post(self, request, *args, **kwargs):
        try:
            Charge.objects.all().delete()
            user = User.objects.get(username__exact = 'admin')
            user.set_password('petrol4ever')
            user.save()
            return Response({"status":"OK"}, status = status.HTTP_200_OK)
        except:
            return Response({"status":"failed"}, status = status.HTTP_400_BAD_REQUEST)


class RightLocationsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.GET
        try:
            address_region1 = data['address_region']
        except:
            return Response({'Not enough parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            time1 = data['time']
            time = datetime.strptime(time1, '%H:%M:%S').time()
        except:
            json = dict()
            locations_query = LocationofStations.objects.filter(address_region=address_region1).all()
            json['LocationsList'] = RightLocationsSerializer(locations_query, many=True).data
            if not json['LocationsList']:
                return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response(json, status=status.HTTP_200_OK)
        json = dict()
        locations_query = LocationofStations.objects.filter(address_region=address_region1, open_hour__lt=time,
                                                            close_hour__gt=time).all()
        json['LocationsList'] = RightLocationsSerializer(locations_query, many=True).data
        if not json['LocationsList']:
            return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(json, status=status.HTTP_200_OK)


class AllLocationsView(APIView):

    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)


        json = dict()
       # distinct = LocationofStations.objects.values('address_region').annotate(name_count=Count('address_region')).filter(name_count=3)
        #locations_query = LocationofStations.objects.filter(address_region__in=[item['address_region'] for item in distinct])
        locations_query = LocationofStations.objects.values('address_region').order_by('address_region').distinct()
        json['LocationsList'] = AllLocationsSerializer(locations_query, many = True).data
        if not json['LocationsList']:
            return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(json, status=status.HTTP_200_OK)


class MonthlyChargesView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        charge_query = MonthlyCharge.objects.filter(user_id_id=user.id, already_paid=0).all()
        json = dict()
        json['ChargesList'] = MonthlyChargesSerializer(charge_query, many=True).data
        if not json['ChargesList']:
            return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(json, status=status.HTTP_200_OK)


class SpecificPointsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.GET
        try:
            locationID = data['location_id']
        except:
            return Response({'Not enough parameters'}, status=status.HTTP_400_BAD_REQUEST)

        json = dict()
        points_query = Station.objects.filter(location_id=locationID, available=1).all()
        json['PointsList'] = SpecificPointsSerializer(points_query, many=True).data
        if not json['PointsList']:
            return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(json, status=status.HTTP_200_OK)


class LocationPointsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.GET
        try:
            locationID = data['location_id']
        except:
            return Response({'Not enough parameters'}, status=status.HTTP_400_BAD_REQUEST)

        json = dict()
        points_query = Station.objects.filter(location_id=locationID).all()
        json['PointsList'] = LocationPointsSerializer(points_query, many=True).data
        if not json['PointsList']:
            return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(json, status=status.HTTP_200_OK)


class IfMonthlyChargesView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        json = dict()
        if_query = MonthlyCharge.objects.filter(user_id_id=user.id).all()
        # json['PointsList'] = LocationPointsSerializer(points_query, many=True).data
        if not if_query:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(status=status.HTTP_200_OK)


class MonthlyChargeUpdatetView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.GET
        try:
            charge_id = data['id']
        except:
            return Response({"Not enough parameters"}, status=status.HTTP_400_BAD_REQUEST)

        MonthlyCharge.objects.filter(pk=charge_id).update(already_paid=1)

        return Response(status=status.HTTP_200_OK)


class ChargeInsertView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            data = request.GET
            station_id = data['station']
            protocol = data['protocol']
            energy_amount = data['energy_amount']
            amount = data['amount']
        except:
            return Response({"Not enough parameters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stationn = Station.objects.get(pk=station_id)
        except:
            return Response({"Invalid StationID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vehicle = Vehicle.objects.get(pk=user.id)
        except:
            return Response({"Invalid StationID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            car = CarOwner.objects.get(pk=user.id)
        except:
            return Response({"Invalid StationID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            method = data['method']
            c = Charge.objects.create(vehicle_carowner_id=vehicle, station_id_id=stationn, started_on=datetime.now(),
                                      finished_on=datetime.now(), energy_amount=energy_amount, amount=amount,
                                      payment_method=method, protocol=protocol)
        except:
            c = Charge.objects.create(vehicle_carowner_id=vehicle, station_id_id=stationn, started_on=datetime.now(),
                                      finished_on=datetime.now(), energy_amount=energy_amount, amount=amount,
                                      payment_method='month bill', protocol=protocol)
            d = MonthlyCharge.objects.create(user_id_id=car, month=datetime.now().month, year=datetime.now().year,
                                             total_amount=amount, already_paid=0)

        return Response(status=status.HTTP_200_OK)


class CarOwnerElementsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        carowner = CarOwner.objects.get(pk=user.id)
        json = dict()
        json['ID'] = user.id
        json['CardNumber'] = CarOwner.objects.get(pk=user.id).card_number
        json['Phone'] = CarOwner.objects.get(pk=user.id).phone
        json['BrandType'] = Vehicle.objects.get(carowner=carowner).brand_type
        json['Model'] = Vehicle.objects.get(carowner=carowner).model
        json['Type'] = Vehicle.objects.get(carowner=carowner).type
        json['ReleaseYear'] = Vehicle.objects.get(carowner=carowner).release_year
        json['UsableBattery'] = Vehicle.objects.get(carowner=carowner).usable_battery_size
        json['KmAfterPrevCharge'] = Vehicle.objects.get(carowner=carowner).km_after_prev_charge

        return Response(json, status=status.HTTP_200_OK)


class EnergyProviderElementsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'EnergyProviders':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        json = dict()
        json['ID'] = user.id
        json['Name'] = EnergyProviders.objects.get(pk=user.id).name
        json['Fast_Charge_Cost'] = EnergyProviders.objects.get(pk=user.id).fast_charge_cost
        json['Slow_Charge_Cost'] = EnergyProviders.objects.get(pk=user.id).slow_charge_cost

        return Response(json, status=status.HTTP_200_OK)


class OperatorElementsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key=token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'ParkingOwner' and group != 'Municipality':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        json = dict()
        json['ID'] = user.id
        if group == 'ParkingOwner':
            json['Name'] = PointOperator.objects.get(pk=user.id).name
        else:
            json['Name'] = Area.objects.get(pk=user.id).name

        return Response(json, status=status.HTTP_200_OK)


class SendAllLocationsView(APIView):
    renderer_classes = [JSONRenderer, CSVRenderer]

    def get(self, request, *args, **kwargs):

        try:
            _, token = request.META.get('HTTP_AUTHORIZATION').split(" ")
        except:
            return Response({'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Token.objects.get(key = token).user
        except:
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)

        group = list(user.groups.values_list('name', flat=True))[0]
        if group != 'CarOwner':
            return Response({'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        json = dict()
        query = LocationofStations.objects.all()
        json['LocList'] = SendAllLocationsSerializer(query, many=True).data
        if not json['LocList']:
            return Response(json, status=status.HTTP_402_PAYMENT_REQUIRED)
        else:
            return Response(json, status=status.HTTP_200_OK)