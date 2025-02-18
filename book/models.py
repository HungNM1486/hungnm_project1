from django.db import models

# Model Danh mục cho sách
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# Model Sách
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    
    # Một cuốn sách có thể thuộc nhiều danh mục
    category = models.ManyToManyField(Category, blank=True)
    
    # Ảnh bìa của sách
    image = models.ImageField(upload_to='books/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_stock(self, quantity):
        self.stock += quantity
        self.save()

    def get_discounted_price(self, discount):
        return self.price * (1 - discount / 100)

    def get_detail(self):
        return {
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'price': self.price,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'publication_date': self.publication_date,
            'stock': self.stock,
            'categories': [cat.name for cat in self.category.all()],
            'image': self.image.url if self.image else None,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __str__(self):
        return self.title
