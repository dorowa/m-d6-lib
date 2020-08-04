from django.contrib import admin
from p_library.models import Book, Author, Publisher, Friend, BorrowBook
from django.utils.html import format_html

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    @staticmethod
    def author_full_name(obj):
        return obj.author.full_name
        
    list_display = ('title','author_full_name','image_tag')
    fields = ('ISBN','title','description','year_release','author', 'publisher','price', 'book_img')

    def image_tag(self, obj):
        if obj.book_img:
            return format_html(f'<img src="{obj.book_img.url}" width="100"/>')
        return format_html(f'<img src="" width="100">')

    image_tag.short_description = 'Обложка'   


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone')
    fields = ('full_name','phone','rating')

@admin.register(BorrowBook)
class BorrowBookAdmin(admin.ModelAdmin):
    list_display = ('book','friend','borrow_date','return_date', 'returned_flag')
