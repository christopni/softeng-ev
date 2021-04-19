"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path

from backendapp.views import *
from django.urls import path, register_converter
from django.conf.urls import url
from backendapp.converters import DateConverter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('evcharge/api/login/',LoginView.as_view(), name = 'login'),
	path('evcharge/api/logout/',LogoutView.as_view(), name = 'logout'),
    path('evcharge/api/SessionsPerPoint/<int:point_id>/<str:start_date>/<str:end_date>/', SessionPerPointView.as_view(), name = 'session_per_point'),
    path('evcharge/api/SessionsPerStation/<int:station_id>/<str:start_date>/<str:end_date>/', SessionPerStationView.as_view(), name = 'session_per_station'),
    path('evcharge/api/SessionsPerEV/<int:vehicle_id>/<str:start_date>/<str:end_date>/', SessionPerEVView.as_view(), name = 'session_per_ev'),
    path('evcharge/api/SessionsPerProvider/<int:provider_id>/<str:start_date>/<str:end_date>/', SessionPerProviderView.as_view(), name = 'session_per_provider'),
    path('evcharge/api/healthcheck/',HealthcheckView.as_view(), name = 'healthcheck'),
    path('evcharge/api/admin/users/<str:username>/', UserElementsView.as_view(), name = 'userelements'),
    path('evcharge/api/admin/usermod/<str:username>/<str:password>/',UsermodView.as_view(),name = 'usermod'),
    path('evcharge/api/statistics/provider/', ProviderStatisticsView.as_view(), name = 'provider_statistics_kallia'),
    path('evcharge/api/statistics/operator/', OperatorStatisticsView.as_view(), name = 'operator_statistics_kallia'),
    path('evcharge/api/operator/location/insert/', OperatorLocationInsertView.as_view(), name = 'operator_insert_location_frosy'),
    path('evcharge/api/operator/station/insert/', OperatorStationInsertView.as_view(), name = 'operator_insert_station_frosy'),
    path('evcharge/api/operator/location/details/',OperatorLocationDetailsView.as_view(), name='operator_location_details_kallia'),
    path('evcharge/api/operator/station/energyproviders/details/',OperatorEnergyProvidersDetailsView.as_view(), name='operator_provider_details_kallia'),
    path('evcharge/api/operator/location/update/', OperatorLocationUpdatetView.as_view(), name = 'operator_update_location_frosy'),
    path('evcharge/api/operator/station/update/', OperatorStationUpdatetView.as_view(), name = 'operator_update_station_frosy'),
    path('evcharge/api/operator/station/delete/', OperatorStationDeleteView.as_view(), name = 'operator_delete_station_frosy'),
    path('evcharge/api/admin/resetsessions/',ResetSessionView.as_view(), name = 'resetsession'),
    path('evcharge/api/carowner/specificlocations/',RightLocationsView.as_view(),name='specific_locations'),
    path('evcharge/api/carowner/all_locations/',AllLocationsView.as_view(),name='locations'),
    path('evcharge/api/carowner/monthly_charges/',MonthlyChargesView.as_view(),name='monthly_charges'),
    path('evcharge/api/carowner/available_points/',SpecificPointsView.as_view(),name='available_points'),
    path('evcharge/api/admin/system/sessionsupd/',SessionsUpdView.as_view(),name = 'sessionsupd'),
    path('evcharge/api/operator/location_points/',LocationPointsView.as_view(),name='location_points'),
    path('evcharge/api/carowner/if_monthly_charges/',IfMonthlyChargesView.as_view(),name='if'),
    path('evcharge/api/carowner/payment_verification/',MonthlyChargeUpdatetView.as_view(),name='verificationofpayment'),
    path('evcharge/api/carowner/chargepayverified/',ChargeInsertView.as_view(),name='insert_charge'),
    path('evcharge/api/carowner/elements/',CarOwnerElementsView.as_view(),name='car_elements'),
    path('evcharge/api/energyprovider/elements/',EnergyProviderElementsView.as_view(),name='energyprovider_elements'),
    path('evcharge/api/operator/elements/',OperatorElementsView.as_view(),name='operator_elements'),
    path('evcharge/api/carowner/all_loc/',SendAllLocationsView.as_view(),name='all_loc')
]
