from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']
   
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    precio = models.IntegerField()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
    