from django.urls import path
from . import views

app_name = 'carefreg'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('provided_services/new/', views.provided_services_detail, name='provided_services_new'),
	path('services/', views.ServicesListView.as_view(), name='services'),
	path('devices/', views.DevicesListView.as_view(), name='devices'),
	path('cartridges/', views.CartridgesListView.as_view(), name='cartridges'),
]
