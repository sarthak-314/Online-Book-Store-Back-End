from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from allauth.account.views import confirm_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    
    path('api/book/', include('books.urls.book', namespace='books')), 
    path('api/bookad/', include('books.urls.bookad', namespace='books')), 
    path('api/user/', include('books.urls.user', namespace='books')), 
    path('api/order/', include('books.urls.order', namespace='books')), 
    path('api/blog/', include('books.urls.blog', namespace='books')), 
    
    re_path(r'rest-auth/registration/account-confirm-email/(?P<key>.+)/', confirm_email, name='account_confirm_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# path('auth/', include('dj_rest_auth.urls')), 
# path('auth/registration', include('dj_rest_auth.registration.urls'))
