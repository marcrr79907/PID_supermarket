from django.forms import ModelForm
from .models import *


class Product_Form(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return data
    
    
class Category_Form(ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
        

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)

        return data
