# Django imports.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View

# Blog app imports
from bank.forms import UserLoginForm

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie



# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = 'account/login.html'
    context_object = {"login_form": UserLoginForm}
    authentication_classes = ()
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        login_form = UserLoginForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Login Successful ! "
                                          f"Welcome {user.username}.")
                return redirect('bank:dashboard_home')

            else:
                messages.error(request,
                               f"Invalid Login details: {username}, {password} "
                               f"are not valid username and password !!! Please "
                               f"enter a valid username and password.")
                return render(request, self.template_name, self.context_object)

        else:
            messages.error(request, f"Invalid username and password")
            return render(request, self.template_name, self.context_object)



