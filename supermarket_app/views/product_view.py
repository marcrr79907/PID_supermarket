from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse_lazy
from ..models import Product, Category
from ..forms import Product_Form, SearchProductForm
from ..mixins import IsSuperuserMixin


class ProductListView(LoginRequiredMixin, IsSuperuserMixin, ListView):
    model = Product
    template_name = 'product/product_template.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        product_list = Product.objects.filter(
            user=self.request.user)

        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Mis Productos'
        context['title'] = 'Agregar Producto'
        context['entity'] = Product
        context['product_list'] = product_list
        context['category_list'] = Category.objects.all()
        context['action'] = 'add'
        context['action_update'] = 'edit'
        context['search_product'] = 'search_product'
        context['data'] = self.request.session.pop('data', None)

        return context


class ProductCreateView(LoginRequiredMixin, IsSuperuserMixin, CreateView):
    model = Product
    form_class = Product_Form
    template_name = 'product/product_template.html'
    success_url = reverse_lazy('supermarket:product_list')

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
                    name=request.POST['name']

                    product_list = Product.objects.filter(user=self.request.user)
                    for product in product_list:

                        if product.name == name:

                            request.session['data'] = {
                            'error_message': 'Ya existe un producto con este nombre!'}
                            return redirect(self.success_url)
                    
                    form.instance.user = self.request.user
                    data['form_is_valid'] = True
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'El producto ha sido creado con éxito.'}
            print(request.session['data'])
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Product'
        context['success_url'] = self.success_url
        
        return context

class ProductUpdateView(LoginRequiredMixin, IsSuperuserMixin, UpdateView):
    model = Product
    form_class = Product_Form
    template_name = 'product/product_template.html'
    success_url = reverse_lazy('supermarket:product_list')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        data['form_is_valid'] = False

        try:
            action = request.POST['action_update']
            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    
                    form.save()
                    data['form_is_valid'] = True

                else:
                    data['error'] = form.errors    
                
            else:
                data['error'] = 'No ha ingresado ninguna acción'
                
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'El producto ha sido actualizado con éxito.'}
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto'

        return context 


class ProductDeleteView(LoginRequiredMixin, IsSuperuserMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('supermarket:product_list')
    template_name = 'eliminar.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
        
        
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        
        context['title'] = 'Eliminar Producto'
        context['text'] = 'Estas seguro que desea eliminar el producto?'
        context['url_redirect'] = self.success_url
        return context
   

class SearchProductView(LoginRequiredMixin, IsSuperuserMixin, TemplateView):
    template_name = 'product/product_template.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        data['form_is_valid'] = False
        try:
            action = request.POST['action']
            if action == 'search_product':
                form = self.get_form()
                
                if form.is_valid():
                    
                    data['form_is_valid'] = True

                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado ninguna acción!'
        
        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'Busqueda exitosa.'}
            print(request.session['data'])
            return redirect(self.success_url)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Buscar Productos:'
        context['form'] = SearchProductForm()
        

        return context