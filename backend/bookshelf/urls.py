from django.urls import path, include
from rest_framework import routers
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.views import TokenRefreshView

from bookshelf import views
from bookshelf.views import MyObtainTokenPairView, RegisterView

app_name = 'bookshelf'

urlpatterns = [
    path('<int:id>/', views.BookAction.as_view()),
    path('', views.BookList.as_view() ),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
