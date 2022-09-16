from bank.forms import UserRegisterForm
from bank.token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from bank.forms import UserLoginForm, CustomerLoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer, Account, PostTransaction, Payment
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail
from itertools import chain
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpResponseNotAllowed
import pandas as pd

# Create your views here.


# def index(request):
    # template_name = 'index.html'
    # context_object = {"customer_login_form": CustomerLoginForm}
    # authentication_classes = ()

    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, self.context_object)

    # def post(self, request, *args, **kwargs):

    #     login_form = CustomerLoginForm(data=request.POST)

    #     if login_form.is_valid():
    #         USER_ID = login_form.cleaned_data['USER_ID']
    #         password = login_form.cleaned_data['password']

    #         user = authenticate(request, USER_ID=USER_ID, password=password)

    #         if user:
    #             login(request, user)
    #             messages.success(request, f"Login Successful ! "
    #                                       f"Welcome {user.USER_ID}.")
    #             return redirect('bank:customerdash_home')

    #         else:
    #             messages.error(request,
    #                            f"Invalid Login details: {USER_ID}, {password} "
    #                            f"are not valid username and password !!! Please "
    #                            f"enter a valid username and password.")
    #             return render(request, self.template_name, self.context_object)

    #     else:
    #         messages.error(request, f"Invalid username and password")
    #         return render(request, self.template_name, self.context_object)
    # # return render(request, 'index.html', {})


class UserCreate(CreateView):
    model = User
    form_class = SignupForm

    def get_success_url(self):
        return reverse('bank:customer-create')


class UserUpdate(UpdateView):
    model = User
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'

    # def get_success_url(self):
    #     return reverse('bank:customer-update', kwargs={'id': self.user_id})


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('users')


class CustomerDetailView(generic.DetailView):
    model = Customer


class CustomerCreate(CreateView):
    model = Customer
    fields = '__all__'

    def get_success_url(self):
        return reverse('bank:account-create')


class CustomerUpdate(UpdateView):
    model = Customer
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    # def get_success_url(self):
    #     return reverse('bank:account-update')


class CustomerListView(generic.ListView):
    model = Customer
    context_object_name = 'customers_list'
    template_name = 'dashboard/author/customer_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """override get_context_data() in order to pass additional
        context variables to the template """

        # Call the base implementation first to get the context
        context = super(CustomerListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        return context


class CustomerDelete(DeleteView):
    model = Customer
    # success_url = reverse_lazy('customers-list')
    template_name = 'dashboard/author/customer_confirm_delete.html'

    def get_success_url(self):
        return reverse('bank:customers-list', kwargs={'pk': self.pk})


class AccountCreate(CreateView):
    model = Account
    fields = '__all__'

    def get_success_url(self):
        return reverse('bank:dashboard_home')


class AccountUpdate(UpdateView):
    model = Account
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'

    def get_success_url(self):
        return reverse('bank:dashboard_home')


class AccountDelete(DeleteView):
    model = Account
    template_name = 'dashboard/author/account_confirm_delete.html'
    # success_url = reverse_lazy('accounts')

    def get_success_url(self):
        return reverse('bank:accounts-list', kwargs={'pk': self.pk})


class AccountDetailView(generic.DetailView):
    model = Account


class AccountListView(generic.ListView):
    model = Account
    context_object_name = 'accounts'
    template_name = 'dashboard/author/account_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """override get_context_data() in order to pass additional
        context variables to the template """

        # Call the base implementation first to get the context
        context = super(AccountListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        return context


class PostTransactionCreate(SuccessMessageMixin, CreateView):
    model = PostTransaction
    fields = '__all__'

    # success_url = '/success/'
    success_message = "Transaction successful"


class PostTransactionUpdate(UpdateView):
    model = PostTransaction
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class PostTransactionDelete(DeleteView):
    model = PostTransaction
    template_name = 'dashboard/author/posttransaction_confirm_delete.html'
    success_url = reverse_lazy('bank:dashboard_home')

    # def get_success_url(self):
    #     return reverse('bank:posttransactions-list', kwargs={'pk': self.pk})


class PostTransactionDetailView(generic.DetailView):
    model = PostTransaction


class PostTransactionListView(generic.ListView):
    model = PostTransaction
    context_object_name = 'posttransactions'
    template_name = 'dashboard/author/posttransaction_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """override get_context_data() in order to pass additional
        context variables to the template """

        # Call the base implementation first to get the context
        context = super(PostTransactionListView,
                        self).get_context_data(**kwargs)
        # Create any data and add it to the context
        return context


# @api_view(['POST'])
class PaymentCreate(SuccessMessageMixin, CreateView):
    model = Payment
    fields = ['account_name', 'account_number', 'bank', 'amount','receiver_email', 'routing_number', 'bank_address', 'otp']
    context = {}
    context_object_name = 'payment'
    template_name = 'bank/payment_form.html'

    
    def get(self, request, *args, **kwargs):
        self.context = super(PaymentCreate, self).get(request, **kwargs)

        transaction_list = PostTransaction.objects.filter(
                account_id=request.user.id).order_by("-date")

        # print(transaction_list)

        payments_sent_list = Payment.objects.all().order_by("-date")

        # print(payments_sent_list)

        # all_transactions = list(chain(transaction_list, payments_sent_list))

        all_withdrawals = sum(
            transaction.amount for transaction in payments_sent_list)
        all_deposits = sum(
            transaction.amount for transaction in transaction_list)

        # pay = get_object_or_404(Payment, kwargs={'pk': self.pk})

        balance = all_deposits - all_withdrawals

        success_message = "Transaction successful"
        if bool(all_deposits <= all_withdrawals) and bool(str(self.model.amount) >= str(balance)):
            return HttpResponse("Transaction Denied - Insufficience balance", status=406)
            # HttpResponse({"Transaction Denied": "Insufficience balance"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            self.context['success_message'] = success_message
        
            return self.context
            
class CustomerPaymentCreate(SuccessMessageMixin, CreateView):
    model = Payment
    fields = ['account_name', 'account_number', 'bank', 'amount','receiver_email', 'routing_number', 'bank_address', 'otp']
    context = {}
    context_object_name = 'payment'
    template_name = 'bank/customer_payment_form.html'

    
    def get(self, request, *args, **kwargs):
        self.context = super(CustomerPaymentCreate, self).get(request, **kwargs)

        transaction_list = PostTransaction.objects.filter(
                account_id=request.user.id).order_by("-date")

        # print(transaction_list)

        payments_sent_list = Payment.objects.all().order_by("-date")

        # print(payments_sent_list)

        # all_transactions = list(chain(transaction_list, payments_sent_list))

        all_withdrawals = sum(
            transaction.amount for transaction in payments_sent_list)
        all_deposits = sum(
            transaction.amount for transaction in transaction_list)

        # pay = get_object_or_404(Payment, kwargs={'pk': self.pk})

        balance = all_deposits - all_withdrawals

        success_message = "Transaction successful"
        if bool(all_deposits <= all_withdrawals) and bool(str(self.model.amount) >= str(balance)):
            return HttpResponse("Transaction Denied - Insufficience balance", status=406)
            # HttpResponse({"Transaction Denied": "Insufficience balance"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            self.context['success_message'] = success_message
        
            return self.context
    


class PaymentUpdate(UpdateView):
    model = Payment
    fields = '__all__'
    # Not recommended (potential security issue if more fields added)
    # exclude = ['error_message']


class PaymentDelete(DeleteView):
    model = Payment
    template_name = 'dashboard/author/payment_confirm_delete.html'
    success_url = reverse_lazy('bank:dashboard_home')

    # def get_success_url(self):
    #     return reverse('bank:payment-list')


class PaymentDetailView(generic.DetailView):
    model = Payment


class PaymentListView(generic.ListView):
    model = Payment
    context_object_name = 'payments'
    template_name = 'dashboard/author/payment_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """override get_context_data() in order to pass additional
        context variables to the template """

        # Call the base implementation first to get the context
        context = super(PaymentListView,
                        self).get_context_data(**kwargs)
        # Create any data and add it to the context
        return context


class DashboardHomeView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'dashboard/author/dashboard_home.html'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        transaction_list = PostTransaction.objects.filter(
            account_id=request.user.id).order_by("-date")

        # print(transaction_list)

        payments_sent_list = Payment.objects.all().order_by("-date")

        # print(payments_sent_list)

        # all_transactions = list(chain(transaction_list, payments_sent_list))

        customers = Customer.objects.all()
        accounts = Account.objects.all()

        login_user_accounts = Account.objects.filter(
            id=request.user.id)
        login_customer = Customer.objects.filter(id=request.user.id)

        all_deposits = sum(
            transaction.amount for transaction in transaction_list)
        all_withdrawals = sum(transaction.amount for transaction in payments_sent_list)

        balance = (sum(transaction.amount for transaction in transaction_list) -
                   sum(transaction.amount for transaction in payments_sent_list))
        # lent_trant = len(transaction_list)
        # len_pay = len(payments_sent_list)
        
        # previous_bal = (sum(transaction.amount for transaction in transaction_list[0:lent_trant]) - sum(transaction.amount for transaction in payments_sent_list[0:len_pay]))

        self.context['all_deposits'] = all_deposits
        self.context['all_withdrawals'] = all_withdrawals
        self.context['transaction_list'] = transaction_list
        self.context['payments_sent_list'] = payments_sent_list
        # self.context['all_transactions'] = all_transactions
        self.context['balance'] = balance
        # self.context['previous_bal'] = previous_bal
        self.context['customers'] = customers
        self.context['accounts'] = accounts
        self.context['login_user_accounts'] = login_user_accounts
        self.context['login_customer'] = login_customer

        return render(request, self.template_name, self.context)


class CustomerProfileView(LoginRequiredMixin, View):
    """
    Displays author profile details
    """
    template_name = "dashboard/author/user_profile_detail.html"
    context_object = {}

    def get(self, request):
        customer = Customer.objects.get(username=request.user)

        self.context_object['user_profile_details'] = customer
        return render(request, self.template_name, self.context_object)


# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = 'registration/login.html'
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
                return redirect('bank:customerdash_home')

            else:
                messages.error(request,
                               f"Invalid Login details: {username}, {password} "
                               f"are not valid username and password !!! Please "
                               f"enter a valid username and password.")
                return render(request, self.template_name, self.context_object)

        else:
            messages.error(request, f"Invalid username and password")
            return render(request, self.template_name, self.context_object)


# Django imports


# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserLogoutView(View):
    """
     Logs user out of the dashboard.
    """
    template_name = 'registration/logout.html'

    def get(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return render(request, self.template_name)


# Django imports.

# Blog app imports.


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserRegisterView(View):
    """
      View to let users register
    """
    template_name = 'registration/register.html'
    context_object = {
        "register_form": UserRegisterForm()
    }

    def get(self, request):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Cadence Bank Account'
            message = render_to_string('registration/account_activation_email.html',
                                       {
                                           'user': user,
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user),
                                       })
            user.email_user(subject, message)

            subject = 'welcome to Cadence Bank'


            message = f'Hi {user.username}, thank you for registering in Cadence Bank.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, 'prosperlekia@gmail.com']
            send_mail(subject, message, email_from, recipient_list)

            return redirect('bank:account_activation_sent')

        else:
            messages.error(request, "Please provide valid information.")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class AccountActivationSentView(View):

    def get(self, request):
        return render(request, 'registration/account_activation_sent.html')


# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ActivateView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()

            login(request, user)

            username = user.username

            messages.success(request, f"Congratulations {username} !!! "
                                      f"Your account was created and activated "
                                      f"successfully"
                             )

            return redirect('bank:login')
        else:
            return render(request, 'registration/account_activation_invalid.html')



@method_decorator(ensure_csrf_cookie, name='dispatch')
class CustomerLoginView(View):
    """
     Logs author into dashboard.
    """
    template_name = 'index.html'
    context_object = {"customer_login_form": CustomerLoginForm}
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):

        login_form = CustomerLoginForm(data=request.POST)

        if login_form.is_valid():
            USER_ID = login_form.cleaned_data['USER_ID']
            password = login_form.cleaned_data['password']

            user = authenticate(request, username=USER_ID, password=password)

            if user:
                login(request, user)
                messages.success(request, f"Login Successful ! "
                                          f"Welcome {user.USER_ID}.")
                return redirect('bank:customerdash_home')

            else:
                messages.error(request,
                               f"Invalid Login details: {USER_ID}, {password} "
                               f"are not valid username and password !!! Please "
                               f"enter a valid username and password.")
                return render(request, self.template_name, self.context_object)

        else:
            messages.error(request, f"Invalid username and password")
            return render(request, self.template_name, self.context_object)


class CustomerDashView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'customer_dashboard/customer_dashboard.html'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        transaction_list = PostTransaction.objects.filter(
            account_id=request.user.id).order_by("-date")

        last_payment_received = transaction_list.last()

        payments_sent_list = Payment.objects.all().order_by("-date")
        last_payment_sent = payments_sent_list.last()

        # print(payments_sent_list)

        # all_transactions = list(chain(transaction_list, payments_sent_list))

        customers = Customer.objects.all()
        accounts = Account.objects.all()

        login_user_accounts = Account.objects.filter(
            id=request.user.id)
        login_customer = Customer.objects.filter(id=request.user.id)

        all_deposits = sum(
            transaction.amount for transaction in transaction_list)
        all_withdrawals = sum(transaction.amount for transaction in payments_sent_list)

        balance = (sum(transaction.amount for transaction in transaction_list) -
                   sum(transaction.amount for transaction in payments_sent_list))

        self.context['all_deposits'] = all_deposits
        self.context['all_withdrawals'] = all_withdrawals
        self.context['transaction_list'] = transaction_list
        self.context['payments_sent_list'] = payments_sent_list
        self.context['last_payment_received'] = last_payment_received
        self.context['last_payment_sent'] = last_payment_sent
        # self.context['all_transactions'] = all_transactions
        self.context['balance'] = balance
        # self.context['previous_bal'] = previous_bal
        self.context['customers'] = customers
        self.context['accounts'] = accounts
        self.context['login_user_accounts'] = login_user_accounts
        self.context['login_customer'] = login_customer

        return render(request, self.template_name, self.context)

class TransactionHistoryView(LoginRequiredMixin, View):
    """
    Display homepage of the dashboard.
    """
    context = {}
    template_name = 'customer_dashboard/customer_transaction_history.html'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        transaction_list = PostTransaction.objects.filter(
            account_id=request.user.id).order_by("-date")

        payments_sent_list = Payment.objects.all().order_by("-date")
        
        transaction_data = {'Date': [], 'Account Name': [], 'Credit': [], 'Debit': []}
        # transaction_data = {}
        for transaction in transaction_list:
            transaction_data['Date'].append(transaction.date)
            if transaction.account:
                transaction_data['Account Name'].append(transaction.account.account_name)
            else:
                transaction_data['Account Name'].append(transaction.account_name)
            transaction_data['Credit'].append('$'+str(transaction.amount))
            transaction_data['Debit'].append('---')
            

        for transaction in payments_sent_list:
            transaction_data['Date'].append(transaction.date)
            transaction_data['Account Name'].append(transaction.account_name)
            transaction_data['Credit'].append('---')
            transaction_data['Debit'].append('-$'+str(transaction.amount))

        transaction_dataframe = pd.DataFrame.from_dict(transaction_data)
        # transaction_dataframe['Date'] = pd.to_datetime(transaction_dataframe.Date)
        transaction_dataframe.style.format({"Date": lambda t: t.strftime("%m/%d/%Y")})
        transaction_dataframe.sort_values(by='Date',ascending=False) 
        # print(transaction_dataframe)

        # all_transactions = list(chain(transaction_list, payments_sent_list))
        # t_data = {}
        # for transaction in all_transactions:
        #     t_data['Date'] = transaction.date
        #     t_data['Amount'] = transaction.amount
            
        # print(all_transactions)

        customers = Customer.objects.all()
        accounts = Account.objects.all()

        login_user_accounts = Account.objects.filter(
            id=request.user.id)
        login_customer = Customer.objects.filter(id=request.user.id)

        all_deposits = sum(
            transaction.amount for transaction in transaction_list)
        all_withdrawals = sum(transaction.amount for transaction in payments_sent_list)

        balance = (sum(transaction.amount for transaction in transaction_list) -
                   sum(transaction.amount for transaction in payments_sent_list))

        self.context['all_deposits'] = all_deposits
        self.context['all_withdrawals'] = all_withdrawals
        self.context['transaction_list'] = transaction_list
        self.context['payments_sent_list'] = payments_sent_list
        
        self.context['transaction_dataframe'] = transaction_dataframe
        self.context['balance'] = balance
        # self.context['previous_bal'] = previous_bal
        self.context['customers'] = customers
        self.context['accounts'] = accounts
        self.context['login_user_accounts'] = login_user_accounts
        self.context['login_customer'] = login_customer

        return render(request, self.template_name, self.context)