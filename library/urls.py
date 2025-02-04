from django.urls import path, include

from . import views

urlpatterns = [
    #path('user_login/', views.user_login, name='user_login'),
    path('', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('logout/', views.logout_user, name='logout'),
    path('admin_home/', views.home, name='home'),
    path('add_book/', views.add_book, name='add_book'),
    path('view_books/', views.view_books, name='view_books'),

    path('request-book/<int:book_id>/', views.request_book, name='request_book'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('process-request/<int:request_id>/', views.process_request, name='process_request'),
    path('mark-returned/<int:request_id>/', views.mark_returned, name='mark_returned'),
]