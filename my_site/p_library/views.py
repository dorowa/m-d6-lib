from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from p_library.models import Book, Publisher, Author, BorrowBook, Friend
from p_library.forms import AuthorForm, BookForm, BorrowBookFormGive, BorrowBookFormBack, FriendFormAdd, BorrowBookFormReturn, BorrowBookFormSet
from p_library.forms import FriendFormEdit, BookFormEdit
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.forms import formset_factory, modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404

def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all()
    biblio_data = {
        "title":"мою библиотеку",
        "books":books,
        "rng3": [i for i in range(100)]
    }
    return HttpResponse(template.render(biblio_data,request))
    
def books_list(request):
    template = loader.get_template('slash.html')
    books = Book.objects.all().order_by('publisher')
    book_data = {
        "title":"Моя библиотека",
        "books":books
    }
    return HttpResponse(template.render(book_data, request))
# Create your views here.
# Код из модуля, улучшеный и почищеный от лишних ветвлений
def book_increment(request):
    if request.method =="POST":
        book_id = request.POST["id"]
        if book_id:
            book = Book.objects.filter(id=book_id).first()
            if book:
                book.copy_count +=1
                book.save()
    return redirect('/index/')

def book_decrement(request):
    if request.method =="POST":
        book_id = request.POST["id"]
        if book_id:
            book = Book.objects.filter(id=book_id).first()
            if book:
                if book.copy_count<1:
                    book.copy_count = 0
                else:
                    book.copy_count -=1
                book.save()
    return redirect('/index/')
# Выдача данных для ветки publishers
def publishers_index(request):
    template = loader.get_template('publishers.html')
    publishers = Publisher.objects.all()
    pub_data = {
        "title":"Мои издательства",
        "publishers":publishers
    }
    return HttpResponse(template.render(pub_data, request))

# Обработка POST запроса для увеличения рейтинга publishers
def publisher_increment(request):
    if request.method =="POST":
        pub_id = request.POST["id"]
        if pub_id:
            pub = Publisher.objects.filter(id=pub_id).first()
            if pub:
                pub.rating +=1
                pub.save()
    return redirect('/publishers/')

# Обработка POST запроса для уменьшения рейтинга publishers
def publisher_decrement(request):
    if request.method =="POST":
        pub_id = request.POST["id"]
        if pub_id:
            pub = Publisher.objects.filter(id=pub_id).first()
            if pub:
                pub.rating -=1
                pub.save()
    return redirect('/publishers/')

class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('p_library:authors_list')
    template_name = 'authors_edit.html'

class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'

class BookAdd(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('index')
    template_name = 'book_add.html'

class BookEdit(UpdateView):
    model = Book
    form_class = BookFormEdit
    success_url = reverse_lazy('main_list')
    template_name = "book_edit.html"

class FriendList(ListView):
    model = Friend
    template_name = 'friends_list.html'

class FriendAdd(CreateView):
    model = Friend
    form_class = FriendFormAdd
    success_url = reverse_lazy('friend_list')
    template_name = 'friends_add.html'

class FriendUpdate(UpdateView):
    model = Friend
    form_class = FriendFormEdit
    success_url = reverse_lazy('friend_list')
    #fields = ["full_name", "phone", "rating"]
    template_name = 'friend_edit.html'

class BorrowBookNew(CreateView):
    model = BorrowBook
    form_class = BorrowBookFormGive
    success_url = reverse_lazy('borrow_book_back')
    template_name = 'borrow_book_new.html'

class BorrowBookBack(ListView):
    queryset = BorrowBook.objects.filter(returned_flag=False).order_by('borrow_date')
    form_class = BorrowBookFormBack
    template_name = 'borrow_book_back.html'

def borrow_book_list(request):
    if request.method=='GET':
        dataset = BorrowBook.objects.filter(returned_flag=True)
        return render(request, 'borrow_book_list.html', {'dataset':dataset})
    return redirect('/')

def borrow_book_return(request,pk):
    borrow = get_object_or_404(BorrowBook, pk = pk)
    if request.method == 'POST':
        form = BorrowBookFormReturn(request.POST)
        if form.is_valid():
            borrow.return_date = form.cleaned_data['return_date']
            borrow.state_after = form.cleaned_data['state_after']
            borrow.returned_flag = True
            borrow.save()
            return HttpResponseRedirect(reverse_lazy('borrow_book_back'))
    else:
        form = BorrowBookFormReturn()
    return render(request, 'borrow_return.html', {'form':form, 'borrow':borrow})


def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:authors_list'))
    else:
        author_formset = AuthorFormSet(prefix = 'authors')
    return render(request, 'manage_authors.html',{'author_formset':author_formset})

def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm,extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method=='POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix = 'books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('p_library:authors_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(request, 'manage_books_authors.html', {'author_formset':author_formset,'book_formset':book_formset})
