from django.urls import path
from books.views.bookad import ( BookADCreateView, BookADDetailView, BookADListView, BookADCategoryListView,
							BookADDeleteView, BookADTextRecognizerView, BookADImageRecognizerView, BookADNGetView)

app_name = 'books'

urlpatterns = [
	path('create-ad/', BookADCreateView.as_view(), name='create-ad'), 
	path('get-ad/<slug>/', BookADDetailView.as_view(), name='get-ad'), 
	path('get-ads/', BookADListView.as_view(), name='get-ads'), 
	path('get-n-ads/<int:skip>/', BookADNGetView.as_view()), 
	path('get-ads-of-cat/<category>', BookADCategoryListView.as_view(), name='get-ads-of-cat'), 
	path('delete-ad/<slug>', BookADDeleteView.as_view(), name='delete-ad'), 
	path('text-recognizer/', BookADTextRecognizerView.as_view(), name='text-recognizer'),
	path('image-recognizer/', BookADImageRecognizerView.as_view(), name='image-recognizer'),
]