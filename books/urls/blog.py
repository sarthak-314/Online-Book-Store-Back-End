from django.urls import path
from books.views.blog import BlogDetailView, BlogCreateView, BlogListView, BlogByTitle, BlogCommentView
app_name = 'books'

urlpatterns = [
    path(':id/', BlogDetailView.as_view()), 
    path('create-blog/', BlogCreateView.as_view()), 
    path('all/', BlogListView.as_view()), 
    path('get-blog-by-title/', BlogByTitle.as_view()), 
    path('post-comment/', BlogCommentView.as_view()), 
]