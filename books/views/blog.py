from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from books.models import Blog, Book, UserProfile, BlogComment
from books.serializers import BlogSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
from rest_framework.parsers import MultiPartParser, FormParser
import books.utils.goodreads as goodreads
import books.utils.google_books


class BlogDetailView(RetrieveAPIView): 
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_class = [AllowAny]

class BlogCreateView(APIView):
    def post(self, request):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        book_title = request.data.get('book_title')
        title = request.data.get('title')
        content = request.data.get('content')
        rating = request.data.get('rating')
        book = Book.objects.get(title=book_title)
        blog = Blog(user=user, book=book, content=content, rating=rating, title=title)
        blog.save()
        return Response(status=HTTP_200_OK)

class BlogListView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

class BlogByTitle(APIView): 
    def post(self, request):
        title = request.data.get('title')
        blog = Blog.objects.get(title=title)
        blog_data = BlogSerializer(blog).data
        message = {
            'blog': blog_data
        }
        return Response(message, status=HTTP_200_OK)


class BlogCommentView(APIView):
    def post(self, request):
        user = request.user
        user_profile_qs = UserProfile.objects.filter(user=user)
        user_profile = user_profile_qs.first()
        title = request.data.get('title')
        blog_qs = Blog.objects.filter(title=title)
        blog = blog_qs.first()
        comment = request.data.get('comment')
        blog_comment = BlogComment(user_profile=user_profile, comment=comment, blog=blog)
        blog_comment.save()
        return Response({'comment': blog_comment.comment}, status=HTTP_200_OK)