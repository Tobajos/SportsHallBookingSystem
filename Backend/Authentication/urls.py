from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('register/',views.RegisterUser.as_view()),
    path('login/',views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)