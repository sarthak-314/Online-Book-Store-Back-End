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

class OrderBookView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request, slug, *args, **kwargs):
		if slug is None: 
			return Response({'message': 'Slug not detected, boi'}, status=HTTP_400_BAD_REQUEST)
		book_ad = get_object_or_404(BookAD, slug=slug)
		book_order_qs = BookOrder.objects.filter(buyer=request.user, book_ad=book_ad, ordered=False)
		if book_order_qs.exists(): 
			return Response({'message': 'You already ordered this book!'})
		book_order = BookOrder(buyer=request.user, book_ad=book_ad)
		book_order.save()
		return Response(status=HTTP_200_OK)


class ReviewOrderedBook(APIView):
	permission_class = [IsAuthenticated]
	def post(self, request, slug, *args, **kwargs):
		book = request.data.get('title')
		
		title = google_books.get_book_title(title)

		try:
			book_order = BookOrder.objects.get(book_ad__slug=slug, buyer=request.user, ordered=False)

		except ObjectDoesNotExist: 
			return Response({'message': 'Order this book to leave a review'}, status=HTTP_400_BAD_REQUEST)
