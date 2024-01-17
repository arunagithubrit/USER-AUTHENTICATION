from django.urls import path
from user import views

urlpatterns=[
    path('register/',views.creation.as_view()),
    path('verify/<str:token>/', views.EmailVerification.as_view(), name='email-verification'),
    
     

]