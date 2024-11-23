# mycar/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/moteur/', views.scrape_moteur, name='scrape_moteur'),
    path('scrape/avito/', views.scrape_avito, name='scrape_avito'),
    path('start-consumer/', views.consume_messages, name='start_consumer'),
    path('api/car_data/', views.CarDataView.as_view(), name='car_data'),
    path('signup_page/', views.signup_page, name='signup_page'),
    path('admin/signup/', views.AdminSignupView.as_view(), name='admin_signup'),
    path('client/signup/', views.ClientSignupView.as_view(), name='client_signup'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('client/dashboard/<int:client_id>/', views.client_dashboard_view, name='client_dashboard'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('api/record_visit/<int:user_id>/<int:car_id>/', views.record_visit, name='record_visit'),
    path('api/record_save/<int:user_id>/<int:car_id>/', views.record_save, name='record_save'),
    path('api/car_details/<int:id>/', views.car_details, name='car_details'),
    path('api/saved_cars/<int:user_id>/', views.get_saved_cars, name='get_saved_cars'),
    path('admin/admin_list/', views.AdminListView.as_view(), name='admin_list'), 
    path('client/client_list', views.ClientListView.as_view(), name='client-list'),
    path('api/car_data/count/', views.get_car_count, name='get_car_count'),
    path('client/count/', views.get_client_count, name='get_client_count'),
    path('api/recommended-cars/<int:user_id>/', views.get_recommendations, name='get_recommendations'),


]
