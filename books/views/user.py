from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from books.models import Book, BookAD, BookOrder, BookRate, UserProfile
from books.serializers import BookSerializer, BookADSerializer, BookRateSerializer, UserProfileSerializer, FuckingImageSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
import requests
import logging
logger = logging.getLogger(__name__)

class UserInfoView(APIView):
	permission_class = [IsAuthenticated]
	def get(self, request, *args, **kwargs):
		return Response({'email': request.user.email})

class UserProfileCreateView(APIView):
	parser_classes = [MultiPartParser, FormParser]
	def post(self, request, *args, **kwargs):
		user = request.user
		user_profile = UserProfile.objects.filter(user=user)
		profile_pic = request.data.get('file')
		user_profile = UserProfile(user=user, profile_pic=profile_pic)
		user_profile.save()
		return Response({'avatar': user_profile.profile_pic}, status=HTTP_200_OK)
		if not profile_pic: 
			return Response({'message': 'No profile pic'}, status=HTTP_400_BAD_REQUEST)
		if 'phone_num' in request.data: 
			phone_num = request.data.get('phone_num')
			user_profile = UserProfile(user=user, profile_pic=profile_pic, phone_num=phone_num)
		user_profile = UserProfile(user=user, profile_pic=profile_pic)
		user_profile.save()
		
		return Response({'avatar': user_profile.profile_pic}, status=HTTP_200_OK)


class UserRateBookList(APIView): 
	permission_class = [IsAuthenticated]
	def get(self, request, *args, **kwargs):
		book_rate_qs = BookRate.objects.filter(user=request.user)
		book_rate_all = BookRateSerializer(book_rate_qs, many=True).data
		return Response({'books': book_rate_all}, status=HTTP_200_OK)


class JustShowMeTheFuckingImage(APIView):
	parser_classes = [MultiPartParser, FormParser]
	serializer = FuckingImageSerializer()
	def post(self, request, *args, **kwargs):
		serializer = FuckingImageSerializer(data=request.data)
		if serializer.is_valid(): 
			return Response({'asas': serializer.data})
		return Response({'aaa': x, 'data': request._request.POST, 'post': request.POST})
	def put(self, request, *args, **kwargs):
		x = request.data.get('profile_pic')
		return Response({'a': x, 'data': request._request.POST, 'post': request.POST})


class UserListView(ListAPIView):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	
