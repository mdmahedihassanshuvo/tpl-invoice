from django.urls import path
from . import views
app_name = 'bill_invoice'
urlpatterns = [path('', views.create, name='create'), path('<int:pk>/', views.detail, name='detail'), path('<int:pk>/markdown/', views.markdown, name='markdown')]
