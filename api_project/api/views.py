from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from .models import Book
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [AllowAny]

class BookViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [IsAuthenticated]