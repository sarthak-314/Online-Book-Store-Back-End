from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from .models import Book, BookAD, BookOrder, BookRate, UserProfile
from .serializers import BookSerializer, BookADSerializer, BookRateSerializer, UserProfileSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
from rest_framework.parsers import MultiPartParser, FormParser
from .book_recognizer import text_based_recognition, image_based_recognition
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

#BOOK AD VIEWS
class BookADCreateView(APIView):
	permission_class = [IsAuthenticated]
	def post(self, request, *args, **kwargs):
		title = request.data.get('title')
		price = request.data.get('price')
		amazon_price = request.data.get('amazon_price')
		try: 
			book = Book.objects.get(title=title)
		except ObjectDoesNotExist:
			#TODO: Get shit from goodreads API
			book = Book(title=title, category='F')
			book.save()
		book_ad = BookAD(book=book, user=request.user, price=price, amazon_price=amazon_price)
		book_ad.save()	
		return Response(status=HTTP_200_OK)

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

URL_TO_CAT = {'fiction': 'F', 'ai': 'A', 'biography': 'B'}
class BookADCategoryListView(APIView):
	permission_class = [AllowAny]
	def get(self, request, category, *args, **kwargs):
		if category is None: 
			return Response({'message': 'Enter a category'})
		category = URL_TO_CAT[category]
		book_ad_qs = BookAD.objects.filter(book__category=category)
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


# TODO: Move it to users api
class UserInfoView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request, *args, **kwargs):
		return Response({'email': request.user.email})

class UserProfileCreateView(APIView):
	parser_classes = (MultiPartParser, FormParser)

	def post(self, request, *args, **kwargs):
		user = request.user
		profile_pic = request.data.get('profile_pic')
		if not profile_pic: 
			return Response({'message': 'No profile pic'}, status=HTTP_400_BAD_REQUEST)
		if 'phone_num' in request.data: 
			phone_num = request.data.get('phone_num')
		user_profile = UserProfile.objects.filter(user=user)
		if user_profile.exists(): 
			user_profile.update(user=user, profile_pic=profile_pic, phone_num=phone_num)
			return Response({'avatar': profile_pic}, status=HTTP_200_OK)
		else: 
			user_profile = UserProfile(user=user, profile_pic=profile_pic, phone_num=phone_num)
			user_profile = UserProfile(user=user, profile_pic=profile_pic)
			user_profile.save()
			return Response(status=HTTP_200_OK)


# class UserProfileView(RetrieveAPIView):
	# def get(self, )

#ORDER BOOK

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


#RATE BOOK
class RateBookView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request, slug, rating, *args, **kwargs):
		try: 
			book = Book.objects.get(slug=slug)
			book_rate, created = BookRate.objects.get_or_create(book=book, user=request.user, rating=int(rating))
			return Response(status=HTTP_200_OK)
		except ObjectDoesNotExist: 
			return Response({'message': 'Book not found?? something went wrong'})

class UserRateBookList(APIView): 
	permission_class = [IsAuthenticated]
	def get(self, request, *args, **kwargs):
		book_rate_qs = BookRate.objects.filter(user=request.user)
		book_rate_all = BookRateSerializer(book_rate_qs, many=True).data
		return Response({'books': book_rate_all}, status=HTTP_200_OK)

#TODO
class ReviewOrderedBook(APIView):
	permission_class = [IsAuthenticated]
	def post(self, request, slug, *args, **kwargs):
		book = request.data.get('title')
		
		title = google_books.get_book_title(title)

		try:
			book_order = BookOrder.objects.get(book_ad__slug=slug, buyer=request.user, ordered=False)

		except ObjectDoesNotExist: 
			return Response({'message': 'Order this book to leave a review'}, status=HTTP_400_BAD_REQUEST)


class GoodreadsAuthView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request):
		autherization_link = goodreads.get_autherization_link()
		response = redirect(autherization_link)
		print(response)
		return response