from django.db import models

# Create your models here.
class Author(models.Model):
    full_name = models.TextField()
    birth_year = models.SmallIntegerField()
    country = models.CharField(max_length=2)
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
    def __str__(self):
        return f"{self.full_name}"

class Publisher(models.Model):
    name = models.TextField()
    description = models.TextField()
    found_date = models.SmallIntegerField()
    property_type = models.TextField(default="private")
    rating = models.SmallIntegerField(default=0)
    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"
    def __str__(self):
        return f"{self.name}"

class Friend(models.Model):
    full_name = models.TextField()
    phone = models.CharField(max_length=13)
    rating = models.SmallIntegerField(default=0)
    class Meta:
        verbose_name = "Друг"
        verbose_name_plural = "Друзья"
    def __str__(self):
        return f"{self.full_name}"

class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.TextField()
    description = models.TextField()
    year_release = models.SmallIntegerField()
    copy_count = models.SmallIntegerField(default=1)
    price = models.DecimalField(default=1, decimal_places=2, max_digits=10)
    book_img = models.ImageField(upload_to='book_cover/', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete = models.CASCADE, related_name='books')
    friend = models.ManyToManyField(Friend,through='BorrowBook',related_name='borrows', blank=True)
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
    def __str__(self):
        return f"{self.title}"

class BorrowBook(models.Model):
    PERFECT = '00%'
    USED = '10%'
    DAMAGED = '50%'
    BOOK_STATE = [
        (PERFECT, "Идеальное состояние"),
        (USED, 'Заметные следы'),
        (DAMAGED, 'Значительное повреждение')
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_book')
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name='borrowed_friend')
    borrow_date = models.DateField() #заполняется при выдаче
    return_date = models.DateField(blank=True, null=True) #заполняется при сдаче
    state_before = models.TextField()
    state_after = models.TextField(blank=True)
    returned_flag = models.BooleanField(default=False)
    penalties = models.CharField(max_length=3, choices=BOOK_STATE, default=PERFECT)
    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
    def __str__(self):
        return f"{self.book.title} - Выдано {self.borrow_date}"
