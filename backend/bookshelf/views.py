from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.generics import  ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from bookshelf.models import Book
from bookshelf.serializers.BookSerializer import BookSerializer
from bookshelf.serializers.userSerializers import MyTokenObtainPairSerializer, RegisterSerializer


# Create your views here.
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class BookList(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['authors', 'year','price']
    ordering_fields = ['year', 'price']
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (AllowAny,)


class BookAction(APIView):
    lookup_url_kwarg = 'id'
    permission_classes = (AllowAny,)
    serializer_class = BookSerializer

    def get(self, request, id, format=None):
        try:
            book = Book.objects.get(id=id)

            book_info = {
                "id": book.id,
                "title": book.title,
                "year": book.year,
                "price": book.price,
                "authors": [{"name": author.name} for author in book.authors.all()],
            }

            return Response(data=book_info, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



    def put(self, request, id, *args, **kwargs):
        book = Book.objects.filter(id=id)
        if book.count() > 0:
            serializer = BookSerializer(book.get(), data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, id, *args, **kwargs):
        book = Book.objects.filter(id=id)
        if book.count() > 0:
            book.delete()
            return Response( status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
