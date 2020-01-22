from django.urls import path
from api import views

urlpatterns = [
    path('api/user-registration/', views.UserRegistration.as_view()),
    path('api/occurrences/', views.OccurrenceList.as_view()),
    path('api/occurrences/<int:pk>/', views.OccurrenceDetail.as_view()),
]