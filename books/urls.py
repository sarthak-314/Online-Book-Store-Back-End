from django.urls import path
from .views import ( BookDetailView, BookListView, BookADCreateView, BookCreateView, UserInfoView, BookADDetailView, BookADListView, OrderBookView, 
						BookADCategoryListView, RateBookView, UserRateBookList, BookADDeleteView, BookADTextRecognizerView, 
						ReviewOrderedBook, BookADImageRecognizerView, GoodreadsAuthView, 
						UserProfileCreateView)

app_name = 'books'

urlpatterns = [
	path('book/<slug>/', BookDetailView.as_view(), name='book'),
	path('', BookListView.as_view(), name='book-list'), 

	path('create-ad/', BookADCreateView.as_view(), name='create-ad'), 
	path('get-ad/<slug>/', BookADDetailView.as_view(), name='get-ad'), 
	path('get-ads/', BookADListView.as_view(), name='get-ads'), 
	path('get-ads-of-cat/<category>', BookADCategoryListView.as_view(), name='get-ads-of-cat'), 
	path('delete-ad/<slug>', BookADDeleteView.as_view(), name='delete-ad'), 
	
	path('text-recognizer/', BookADTextRecognizerView.as_view(), name='text-recognizer'),
	path('image-recognizer/', BookADImageRecognizerView.as_view(), name='image-recognizer'),

	path('rate-book/<slug>/<rating>/', RateBookView.as_view(), name='rate-book'), 
	path('get-book-ratings/', UserRateBookList.as_view(), name='get-book-ratings'), 
	path('review/<slug>/', ReviewOrderedBook.as_view(), name='review'), 

	path('create-book/', BookCreateView.as_view(), name='create-book'), 
	path('order/<slug>/', OrderBookView.as_view(), name='order'), 

	path('userboi/', UserInfoView.as_view()), 
	path('create-profile/', UserProfileCreateView.as_view(), name='create-profile'), 
	
	
	path('goodreads-auth/', GoodreadsAuthView.as_view(), name='goodreads-auth'), 
	
]