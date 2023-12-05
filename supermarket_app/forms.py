from django.forms import *
from .models import *


class Product_Form(ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'precio', 'category']
        

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
    
    
class SearchProductForm(Form):
    category = ModelChoiceField(queryset=Category.objects.all())
    products = ModelChoiceField(queryset=Product.objects.none())
    