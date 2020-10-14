from django.urls import path
from books.views.order import OrderBookView, ReviewOrderedBook 

app_name = 'books'

urlpatterns = [
	path('review/<slug>/', ReviewOrderedBook.as_view(), name='review'), 
	path('order/<slug>/', OrderBookView.as_view(), name='order'), 	
]