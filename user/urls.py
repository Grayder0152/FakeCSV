from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginFormViews.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
