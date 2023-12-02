from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from ..models import *
from ..forms import *


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'card/credit_card.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cards_list = Product.objects.filter(
            user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Productos'
        context['title'] = 'Agregar Producto'
        context['entity'] = Product
        context['object_list'] = cards_list
        context['action'] = 'add'
        context['data'] = self.request.session.pop('data', None)

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = Product_Form
    template_name = 'card/credit_card.html'
    success_url = reverse_lazy('system:card_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        data['form_is_valid'] = False
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()

                if form.is_valid():
                    print('valid')
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        
        except Product.DoesNotExist:
            data['error'] = 'La tarjeta de no existe'
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'La tarjeta ha sido creada con éxito.'}
            print(request.session['data'])
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Product'
        context['list_url'] = reverse_lazy('product_create')

        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('system:card_list')
    template_name = 'eliminar.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        
        context['title'] = 'Eliminar Productp'
        context['text'] = 'Estas seguro que desea eliminar el producto?'
        context['url_redirect'] = self.success_url
        return context
   