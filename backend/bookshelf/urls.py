from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView


from bookshelf.views import bookView
from bookshelf.views.userView import MyObtainTokenPairView, RegisterView

app_name = 'bookshelf'

urlpatterns = [
    path('ai/<int:id>/', bookView.BookDetails.as_view()),
    path('<int:id>/', bookView.BookAction.as_view()),
    path('<int:id>/review/', bookView.BookReview.as_view()),
    path('', bookView.BookList.as_view()),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
