from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('khoj-search/', views.khoj_search, name='khoj_search'),
    path('api/get-all-input-values/', views.GetAllInputValuesView.as_view(), name='api_get_all_input_values'),
]