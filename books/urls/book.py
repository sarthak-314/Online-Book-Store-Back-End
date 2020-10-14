from django.urls import path
from books.views.book import BookDetailView, BookListView, BookCreateView, GoodreadsAuthView, RateBookView

app_name = 'books'

urlpatterns = [
	path('book/<slug>/', BookDetailView.as_view(), name='book'),
	path('create-book/', BookCreateView.as_view(), name='create-book'), 
	path('all-books/', BookListView.as_view(), name='book-list'), 
	
    path('rate-book/<slug>/<rating>/', RateBookView.as_view(), name='rate-book'), 
	path('goodreads-auth/', GoodreadsAuthView.as_view(), name='goodreads-auth'), 	
]