from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from MANAGE_PRODUCTS import settings


class UsersLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingrese usuario y contraseña'
        return context

class RegisterView(CreateView):

    model = User
    form_class = UserCreationForm
    template_name = 'register.html'
    url_redirect = reverse_lazy('users:register')

   
    def post(self, request, *args, **kwargs):
        data = {}
        data['form_is_valid'] = False
        
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                
                if form.is_valid():

                    if request.POST['password1'] == request.POST['password2']:
                        
                        form.save()
                        data['form_is_valid'] = True

                    else:
                        data['error'] = 'Los campos de contraseña no coinciden!'

                else:
                    data['error'] = form.errors

            else:
                data['error'] = 'No ha ingresado ninguna acción!'

        except Exception as e:
            data['error'] = str(e)

        if data['form_is_valid']:
            request.session['data'] = {
                'success_message': 'La cuenta ha sido creada con éxito.'}
            return redirect(self.url_redirect)
        else:
            request.session['data'] = {
                'error_message': data['error']}
            return redirect(self.url_redirect)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crea una cuenta'
        context['list_url'] = reverse_lazy('register')
        context['action'] = 'add'
        context['data'] = self.request.session.pop('data', None)

        return context
  
