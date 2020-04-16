from django.urls import path
from . import views

app_name = 'carefreg'
urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
	path('services/', views.ServicesListView.as_view(), name='services'),
]