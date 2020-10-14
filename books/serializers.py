from rest_framework import serializers
from .models import Book, BookAD, BookOrder, BookRate, UserProfile, Blog, ImageBoi
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
	category = serializers.SerializerMethodField()
	class Meta: 
		model = Book
		fields = ['id', 'author', 'title', 'category', 'slug', 'image', 'description']

	def get_category(self, obj):
		return obj.get_category_display()


class BookADSerializer(serializers.ModelSerializer):
	book = serializers.SerializerMethodField()
	condition = serializers.SerializerMethodField()
	class Meta: 
		model = BookAD
		fields = ['id', 'book', 'price', 'amazon_price', 'sold', 'condition', 'votes', 'slug']

	def get_book(self, obj):
		return BookSerializer(obj.book).data

	def get_condition(self, obj):
		return obj.get_condition_display()

class BookRateSerializer(serializers.ModelSerializer):
	book = serializers.SerializerMethodField()
	class Meta: 
		model = BookRate
		fields = ['book', 'rating', 'user', 'rate_date']
	def get_book(self, obj):
		return BookSerializer(obj.book).data		


class UserSerializer(serializers.ModelSerializer):
	class Meta: 
		model = User
		fields=['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
	user = serializers.SerializerMethodField()
	class Meta: 
		model = UserProfile
		fields = ['user', 'profile_pic', 'phone_num']
	def get_user(self, obj):
		return UserSerializer(obj.user).data

class BlogSerializer(serializers.ModelSerializer):
	book = serializers.SerializerMethodField()
	user_profile = serializers.SerializerMethodField()
	class Meta: 
		model = Blog
		fields = ['title', 'user_profile', 'rating', 'content', 'book']
	def get_book(self, obj):
		return BookSerializer(obj.book).data
	def get_user_profile(self, obj):
		return UserProfileSerializer(obj.user_profile).data

class FuckingImageSerializer(serializers.ModelSerializer):
	class Meta: 
		model = ImageBoi
		fields = ['image']
		