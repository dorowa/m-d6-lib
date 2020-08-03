"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from p_library import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns =[ 
    path('admin/', admin.site.urls),
    path('', views.books_list, name = 'main_list'),
    path('index/',views.index, name='index'),
    path('index/book_increment/',views.book_increment),
    path('index/book_decrement/',views.book_decrement),
    path('publishers/',views.publishers_index), #url для издательства
    path('publishers/publisher_increment/',views.publisher_increment), #url для увеличения рейтинга издательства
    path('publishers/publisher_decrement/',views.publisher_decrement), #url для уменьшения рейтинга издательства
    path('borrow/new',views.BorrowBookNew.as_view(),name = 'borrow_book_new'),
    path('borrow/list',views.BorrowBookBack.as_view(),name = 'borrow_book_back'),
    path('borrow/list2',views.borrow_book_list, name = 'borrow_book_list'),
    path('borrow/return/<int:pk>',views.borrow_book_return, name='borrow_book_return'),
    path('friend/list',views.FriendList.as_view(), name = 'friend_list'),
    path('friend/add',views.FriendAdd.as_view(), name = 'friend_add'),
    path('friend/edit/<int:pk>',views.FriendUpdate.as_view(), name = 'friend_edit'),
    path('book/add',views.BookAdd.as_view(), name = 'book_add'),
    path('book/edit/<int:pk>',views.BookEdit.as_view(), name = 'book_edit'),
    path('author/',include('p_library.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)