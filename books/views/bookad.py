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
from books.book_recognizer import text_based_recognition, image_based_recognition
import books.utils.goodreads as goodreads
import books.utils.google_books

#user, book, price, amazon_price, condition, sold, slug, ad_image, votes
#BOOK - Title, author, category, slug, image, description

class BookADCreateView(APIView):
	permission_class = [IsAuthenticated]
	parser_classes = [MultiPartParser, FormParser]
	def post(self, request, *args, **kwargs):
		title = request.data.get('title')
		condition = request.data.get('condition')
		category = request.data.get('category')
		price = request.data.get('price')
		bookad_image = request.data.get('image')
		try: 
			book = Book.objects.get(title=title)
		except ObjectDoesNotExist:
			title, description, author, _ = google_books.get_book_info(title)
			book_image = google_books.get_book_image(title)
			#TODO: Make the image in the book as book_image 
			book = Book(title=title, description=description, author=author, 
			category=category, image=bookad_image)
			book.save()
		
		book_ad = BookAD(book=book, user=request.user, price=price, ad_image=bookad_image)
		book_ad.save()	
		return Response(status=HTTP_200_OK)





class BookADDetailView(APIView):
	permission_class = [AllowAny]
	def get(self, request, slug, *args, **kwargs):
		if slug is None: 
			return Response('shit')
		book_ad = BookAD.objects.filter(slug=slug)
		if book_ad.exists(): 
			book_ad_data = BookADSerializer(book_ad.first()).data
			return Response({'book_ad': book_ad_data}, status=HTTP_200_OK)
		else:	
			return Response({'message': 'cannot find the bookad'}, status=HTTP_400_BAD_REQUEST)

class BookADListView(ListAPIView):
	queryset = BookAD.objects.all()
	serializer_class = BookADSerializer
	permission_class = [AllowAny]

URL_TO_CAT = {'fiction': 'F', 'ai': 'A', 'biography': 'B', 'philosophy': 'P', 'science': 'S'}
class BookADCategoryListView(APIView):
	permission_class = [AllowAny]
	def get(self, request, category, *args, **kwargs):
		if category is None: 
			return Response({'message': 'Enter a category'})
		category = URL_TO_CAT[category]
		book_ad_qs = BookAD.objects.filter(book__category=category)
		if len(book_ad_qs) > 10: 
			book_ad_qs = book_ad_qs[:10]
		book_ads = BookADSerializer(book_ad_qs, many=True).data
		return Response(book_ads, status=HTTP_200_OK)

class BookADDeleteView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request, slug, *args, **kwargs):
		if slug is None: 
			return Response('No slug')
		book_ad = BookAD.objects.filter(slug=slug)
		if book_ad.exists():
			book_ad.delete()
			return Response(status=HTTP_200_OK)
		return Response({'message': 'Book not found'}, status=HTTP_400_BAD_REQUEST)


class BookADTextRecognizerView(APIView):
	permission_class = [AllowAny]
	def post(self, request):
		# return Response({'s':'a'}, status=HTTP_200_OK)
		image = request.data.get('image')
		title = text_based_recognition(image)
		title, description, author, category = google_books.get_book_info(title)
		data = {'title':title, 'description': description, 'category':category}
		return Response({'data':data}, status=HTTP_200_OK)

class BookADImageRecognizerView(APIView):
	permission_class = [AllowAny]
	def post(self, request):
		image = request.data.get('image')
		title = image_based_recognition(image)
		title, description, author, category = google_books.get_book_info(title)
		data = {'title':title, 'description': description, 'category':category}
		return Response({'data':data}, status=HTTP_200_OK)


class BookADNGetView(APIView): 
	def get(self, request, skip):
		if skip == 0: 
			book_ads = BookAD.objects.all()[:10]
		book_ad_qs = BookAD.objects.all()[skip : skip + 5]
		book_ads = BookADSerializer(book_ad_qs, many=True).data
		return Response({'ads': book_ads})

