from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from books.models import Book, BookAD, BookOrder, BookRate, UserProfile
from books.serializers import BookSerializer, BookADSerializer, BookRateSerializer, UserProfileSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
from rest_framework.parsers import MultiPartParser, FormParser
import books.utils.goodreads as goodreads
import books.utils.google_books

class BookDetailView(RetrieveAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_class = (AllowAny, )

class BookListView(ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_class = [AllowAny]

class BookCreateView(CreateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	#TODO: Change this
	permission_class = [AllowAny]

class RateBookView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request, slug, rating, *args, **kwargs):
		try: 
			book = Book.objects.get(slug=slug)
			book_rate, created = BookRate.objects.get_or_create(book=book, user=request.user, rating=int(rating))
			return Response(status=HTTP_200_OK)
		except ObjectDoesNotExist: 
			return Response({'message': 'Book not found?? something went wrong'})


class GoodreadsAuthView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request):
		autherization_link = goodreads.get_autherization_link()
		response = redirect(autherization_link)
		print(response)
		return response