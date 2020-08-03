from django import forms
from p_library.models import Author, Book, BorrowBook, Friend
from django.utils.translation import gettext_lazy as _

class AuthorForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput, label="Имя")
#    required_css_class = 'list-group-item'
    class Meta:
        model = Author
        fields = '__all__'
        labels = {
            "birth_year":_("Год рождения"),
            "country":_("Страна")
        }

class BookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput, label="Название")
    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'ISBN':_("Код ISBN"),
            'author':_("Автор"),
            'publisher':_("Издательство"),
            'description':_('Описание'),
            'year_release':_('Год издания'),
            'copy_count':_('Экз.(шт.)'),
            'price':_('Цена'),
            'book_img':_('Обложка'),
        } #подписи полей на форме вывода
        exclude = ('friend',)

class BookFormEdit(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput, label="Название")
    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'ISBN':_("Код ISBN"),
            'author':_("Автор"),
            'friend':_('Друг'),
            'publisher':_("Издательство"),
            'description':_('Описание'),
            'year_release':_('Год издания'),
            'copy_count':_('Экз.(шт.)'),
            'price':_('Цена'),
            'book_img':_('Обложка'),
        } #подписи полей на форме вывода


class BorrowBookFormGive(forms.ModelForm):
    class Meta:
        model = BorrowBook
        fields = ['book', 'friend','borrow_date',
        'state_before']
        labels = {
            'book':_("Книга"),
            'friend':_("Должник"),
            'borrow_date':_("Дата выдачи"),
            'state_before':_("Состояние книги"),
        } #подписи полей на форме вывода
        widgets = {
            #'borrow_date': forms.DateInput(format='%Y-%m-%d', attrs={'type':'date','placeholder':'mm/dd/yyyy' }),
            'borrow_date': forms.SelectDateWidget(empty_label="Nothing"),
            'state_before': forms.TextInput(),
        } #виджеты на форме

class BorrowBookFormBack(forms.ModelForm):
    class Meta:
        model = BorrowBook
        fields = '__all__'

class BorrowBookFormReturn(forms.Form):
    return_date = forms.DateField(required=True, label="Дата возврата", widget=forms.SelectDateWidget(empty_label="Nothing"))
    #return_date = forms.DateField(required=True, label="Дата возврата", widget=forms.DateInput(format='%m/%d/%Y',attrs={'type':'date','placeholder':'yyyy-mm-dd' }))
    state_after = forms.CharField(required=True, label="Состояние книги")
    returned_flad = forms.BooleanField(initial=True, required=True, label="Принято")
    class Meta:
        pass

class FriendFormAdd(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput, label="Полное имя")
    class Meta:
        model = Friend
        fields = '__all__'
        labels = {
            "phone":_("Телефон"),
            "rating":_("Рейтинг"),
        }
class FriendFormEdit(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput, label="Полное имя")
    class Meta:
        model = Friend
        fields = "__all__"
        labels = {
            'phone':_("Телефон"),
            'rating':_("Рейтинг"),
        }

BorrowBookFormSet = forms.modelformset_factory(BorrowBook, fields=('book','friend','borrow_date'),
        widgets={'borrow_date':forms.TextInput()})