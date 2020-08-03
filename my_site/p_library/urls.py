from django.contrib import admin
from django.urls import path
from .views import AuthorEdit, AuthorList, author_create_many, books_authors_create_many

app_name = 'p_library'
urlpatterns = [
    path('create', AuthorEdit.as_view(), name='authors_create'),
    path('list', AuthorList.as_view(), name='authors_list'),
    path('multiple', author_create_many, name='author_create_many'),
    path('multiple_books',books_authors_create_many, name='author_book_create_many'),
]