from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('reservation/',views.ReservationView.as_view()),
    path('reservation/<int:reservation_id>/',views.ReservationView.as_view()),
    path('reservations/',views.AllReservationsView.as_view()),
    path('post/',views.PostView.as_view()),
    path('post/<int:post_id>/',views.PostView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)