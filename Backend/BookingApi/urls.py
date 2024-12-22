from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('reservation/',views.ReservationView.as_view()),
    path('reservation/<int:reservation_id>/',views.ReservationView.as_view()),
    path('reservations/',views.AllReservationsView.as_view()),
    path('reservation/<int:reservation_id>/join/', views.JoinReservationView.as_view()),
    path('reservations/joined/', views.ParticipantReservationsView.as_view()),
    path('reservation/<int:reservation_id>/leave/', views.LeaveReservationView.as_view()),
    path('reservation/<int:reservation_id>/participant/<int:user_id>/remove/', views.ReservationParticipantView.as_view()),

    path('post/',views.PostView.as_view()),
    path('post/<int:post_id>/',views.PostView.as_view()),
    path('posts/', views.AllPostView.as_view()),
    
    path('post/<int:post_id>/comments/', views.CommentView.as_view()),  
    path('comment/<int:comment_id>/', views.CommentView.as_view()),  
    path('comments/', views.AllCommentView.as_view()),  
 
]

urlpatterns = format_suffix_patterns(urlpatterns)