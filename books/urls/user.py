from django.urls import path
from books.views.user import (UserInfoView, UserRateBookList, UserProfileCreateView, 
JustShowMeTheFuckingImage, UserListView)
# Full Stack 

app_name = 'books'

urlpatterns = [
	path('user/', UserInfoView.as_view(), name='user'), 
	path('create-profile/', UserProfileCreateView.as_view(), name='create-profile'), 
	path('rated-books/', UserRateBookList.as_view(), name='rated-books'), 
	path('just-show-me-the-fucking-image/', JustShowMeTheFuckingImage.as_view()), 
	path('all/', UserListView.as_view())
]