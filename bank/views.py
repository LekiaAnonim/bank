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
from bank.forms import UserLoginForm, CustomerLoginForm, CreateHistoryForm, CustomerPaymentForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer, Account, PostTransaction, Payment, CreateHistory
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
from cloudinary.forms import cl_init_js_callbacks
from bootstrap_datepicker_plus.widgets import DatePickerInput


# Create your views here.
handler404 = 'mysite.views.my_custom_page_not_found_view'
handler500 = 'mysite.views.my_custom_error_view'
handler403 = 'mysite.views.my_custom_permission_denied_view'


class UserCreate(CreateView):
    model = User
    form_class = SignupForm

    def get_success_url(self):
        return reverse('bank:customer-create')


class CustomerUserUpdate(UpdateView):
    model = User
    # Not recommended (potential security issue if more fields added)
    fields = ['username', 'first_name', 'last_name', 'email']

    context = {}
    context_object_name = 'user'
    template_name = 'auth/customer_userupdate_form.html'

    def get(self, request, *args, **kwargs):
        self.context = super(CustomerUserUpdate,
                             self).get(request, **kwargs)

        success_message = "Profile update successful"

        self.context['success_message'] = success_message

        return self.context

    def get_success_url(self):
        return reverse('bank:customerdash_home')


class UserUpdate(UpdateView):
    model = User
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'

    def get_success_url(self):
        return reverse('bank:dashboard_home')


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('users')


class CustomerDetailView(generic.DetailView):
    model = Customer


class CustomerCreate(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['user', 'middle_name', 'DOB', 'SSN', 'mobile_number', 'image']

    def get_form(self):
        form = super().get_form()
        form.fields['DOB'].widget = DatePickerInput()
        return form

    def get_success_url(self):
        return reverse('bank:account-create')


class EnrolCustomerCreate(CreateView):
    model = Customer
    fields = ['middle_name', 'DOB', 'SSN', 'mobile_number', 'image']
    template_name = 'bank/enrol_customer_form.html'
    context = {}
    context_object_name = 'customer'

    def get_form(self):
        form = super().get_form()
        form.fields['DOB'].widget = DateTimePickerInput()
        return form

    def get(self, request, *args, **kwargs):
        self.context = super(EnrolCustomerCreate,
                             self).get(request, **kwargs)

        success_message = "Profile update successful"

        self.context['success_message'] = success_message

        return self.context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bank:enrol-account-create')


class CustomerUpdate(UpdateView):
    model = Customer
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'

    def get_form(self):
        form = super().get_form()
        form.fields['DOB'].widget = DatePickerInput()
        return form

    def get_success_url(self):
        return reverse('bank:dashboard_home')


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
        return reverse('bank:dashboard_home')


class AccountCreate(CreateView):
    model = Account
    fields = '__all__'

    def get_success_url(self):
        return reverse('bank:dashboard_home')


class EnrolAccountCreate(CreateView):
    model = Account
    fields = ['account_type', 'account_number']
    context = {}
    context_object_name = 'account'
    template_name = 'bank/enrol_account_form.html'

    def form_valid(self, form):
        # form.instance.user = self.request.user
        if form.instance.account_number != '200220191994':

            messages.error(self.request,
                           f"Enter the correct account number. "
                           f"Or Kindly contact the administrator for the issuance of an account number  "
                           )
            return render(self.request, self.template_name, self.context)

        else:

            return super().form_valid(form)

    def get_success_url(self):
        return reverse('bank:login')


class AccountUpdate(UpdateView):
    model = Account
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    template_name = 'bank/account_form.html'

    def get_context_data(self, **kwargs):
        context = super(AccountUpdate, self).get_context_data(**kwargs)
        accounts = Account.objects.all()
        context['user_model'] = User
        context['customer_model'] = Customer
        context['accounts'] = accounts
        return context

    def get_success_url(self):
        return reverse('bank:dashboard_home')


class AccountDelete(DeleteView):
    model = Account
    template_name = 'dashboard/author/account_confirm_delete.html'

    def get_success_url(self):
        return reverse('bank:dashboard_home')


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
    success_message = "Transaction successful"

    def get_success_url(self):
        return reverse('bank:dashboard_home')


class TransactionHistoryCreate(SuccessMessageMixin, CreateView):
    form_class = CreateHistoryForm
    model = CreateHistory
    # fields = '__all__'
    template_name = 'bank/createttransactionhistory_form.html'

    # success_url = '/success/'
    success_message = "Transaction successful"

    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['date'].widget = DatePickerInput()
    #     return form

    def get_success_url(self):
        return reverse('bank:dashboard_home')


class PostTransactionUpdate(UpdateView):
    model = PostTransaction
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class PostTransactionDelete(DeleteView):
    model = PostTransaction
    template_name = 'dashboard/author/posttransaction_confirm_delete.html'
    success_url = reverse_lazy('bank:dashboard_home')


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


class PaymentCreate(SuccessMessageMixin, CreateView):
    model = Payment
    fields = ['account_name', 'account_number', 'bank', 'amount',
              'receiver_email', 'routing_number', 'bank_address', 'otp']
    context = {}
    context_object_name = 'payment'
    template_name = 'bank/payment_form.html'

    # def form_valid(self, form):
    #     form.instance.account.customer.user = self.request.user
    #     return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.context = super(PaymentCreate, self).get(request, **kwargs)

        transaction_list = PostTransaction.objects.filter(
            account__customer__user_id=request.user.id)

        transaction_history_list = CreateHistory.objects.filter(
            account__customer__user_id=request.user.id)

        payments_sent_list = Payment.objects.filter(
            account__customer__user_id=request.user.id)

        debit_transaction_history_list = transaction_history_list.filter(
            top_up_type='Debit')
        credit_transaction_history_list = transaction_history_list.filter(
            top_up_type='Credit')


        all_withdrawals = sum(
            transaction.amount for transaction in payments_sent_list) + sum(
            transaction.amount for transaction in debit_transaction_history_list)

        all_deposits = sum(
            transaction.amount for transaction in credit_transaction_history_list) + sum(
            transaction.amount for transaction in transaction_list)

        account_suspend = Account.objects.filter(
            customer__user__username=username, suspend_account=True)

        if account_suspend:
            messages.error(request, account_suspend.suspend_account_message)
            return render(request, self.template_name, self.context_object)

        else:

            balance = all_deposits - all_withdrawals

            success_message = "Transaction successful"
            if bool(balance <= 0) and bool(str(self.model.amount) >= str(balance)):
                return HttpResponse("Transaction Denied - Insufficience balance", status=406)
                # HttpResponse({"Transaction Denied": "Insufficience balance"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                self.context['success_message'] = success_message

                return self.context

        def get_success_url(self):
            return reverse('bank:dashboard_home')

# def suspend_account(request):
#     context = {}
#     account_suspend = Account.objects.filter(
#         customer__user__username=request.user.username, suspend_account=True)
#     message = messages.error(
#                 request, account_suspend[0].suspend_account_message)
#             # return HttpResponse(account_suspend[0].suspend_account_message, status=406)
#     context['account_suspend'] = account_suspend
#     context['message'] = message
#     return render(request, 'bank/suspend_error.html', context)


class SuspendAccount(LoginRequiredMixin, View):
    """
    Displays Suspend Account Error Message
    """
    template_name = "bank/suspend_error.html"
    context = {}

    def get(self, request):
        account_suspend = Account.objects.filter(
            customer__user__username=request.user.username, suspend_account=True)
        message = messages.error(
            request, account_suspend[0].suspend_account_message)
        # return HttpResponse(account_suspend[0].suspend_account_message, status=406)
        self.context['account_suspend'] = account_suspend
        self.context['message'] = message
        return render(request, self.template_name, self.context)


class CustomerPaymentCreate(SuccessMessageMixin, CreateView):
    model = Payment
    fields = ['account_name', 'account_number', 'bank', 'amount',
              'receiver_email', 'routing_number', 'bank_address', 'otp']
    context = {}
    context_object_name = 'payment'
    template_name = 'bank/customer_payment_form.html'

    def get(self, request, *args, **kwargs):
        self.context = super(CustomerPaymentCreate,
                             self).get(request, **kwargs)
        message = "Transaction successful"
        self.context['message'] = message
        return self.context

    def post(self, request, *args, **kwargs):

        account_suspend = Account.objects.filter(
            customer__user__username=request.user.username, suspend_account=True)

        transaction_list = PostTransaction.objects.filter(
            account__customer__user_id=request.user.id)

        transaction_history_list = CreateHistory.objects.filter(
            account__customer__user_id=request.user.id)

        payments_sent_list = Payment.objects.filter(
            account__customer__user_id=request.user.id)

        debit_transaction_history_list = transaction_history_list.filter(
            top_up_type='Debit')
        credit_transaction_history_list = transaction_history_list.filter(
            top_up_type='Credit')

        payments_sent_list = Payment.objects.all().order_by("-date")

        all_withdrawals = sum(
            transaction.amount for transaction in payments_sent_list) + sum(
            transaction.amount for transaction in debit_transaction_history_list)

        all_deposits = sum(
            transaction.amount for transaction in credit_transaction_history_list) + sum(
            transaction.amount for transaction in transaction_list)

        # all_withdrawals = sum(
        #     transaction.amount for transaction in payments_sent_list)

        # all_deposits = sum(
        #     transaction.amount for transaction in transaction_list)

        balance = all_deposits - all_withdrawals

        
        if bool(all_deposits <= all_withdrawals) and bool(str(self.model.amount) >= str(balance)):
            return HttpResponse("Transaction Denied - Insufficience balance", status=406)
        else:
            
            if account_suspend:
                return redirect('bank:suspend_account')
            else:
                # self.context = super(CustomerPaymentCreate,
                #                      self).post(request, **kwargs)
                
                
                # return render(request, self.template_name, self.context)
                return super(CustomerPaymentCreate, self).post(request)

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bank:transaction_history')


class PaymentUpdate(UpdateView):
    model = Payment
    fields = '__all__'


class PaymentDelete(DeleteView):
    model = Payment
    template_name = 'dashboard/author/payment_confirm_delete.html'
    success_url = reverse_lazy('bank:dashboard_home')


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
    model = Account
    context = {}
    template_name = 'dashboard/author/dashboard_home.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        customers = Customer.objects.all()
        accounts = Account.objects.all()

        login_user_accounts = Account.objects.filter(
            customer_id=request.user.id)
        login_customer = Customer.objects.filter(id=request.user.id)
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
            account_block = Account.objects.filter(
                customer__user__username=username, block_account=True)

            self.context_object['account_block'] = account_block

            user = authenticate(request, username=username, password=password)

            if user:
                if account_block:
                    messages.error(
                        request, account_block[0].block_account_message)
                    return render(request, self.template_name, self.context_object)

                else:
                    login(request, user)
                    messages.success(request, f"Login Successful ! "
                                     f"Welcome {user.username}. Update your User profile if you have not done so. Ignore this message if your User profile is upto date.")
                    if user.is_superuser == True:
                        return redirect('bank:dashboard_home')
                    else:
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
            user.is_active = True
            user.is_staff = True
            user.save()
            login(request, user)
            messages.success(
                request, f'Hi {user.username}, thank you for registering forSkyHigh Premium online Banking.')

            return redirect('bank:enrol-customer-create')

        else:
            messages.error(request, "Please provide valid information.")
            # Redirect user to register page
            return render(request, self.template_name, self.context_object)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class AccountActivationSentView(View):

    def get(self, request):
        return render(request, 'registration/account_activation_sent.html')


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
     Logs customer into dashboard.
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
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        transaction_list = PostTransaction.objects.filter(
            account__customer__user_id=request.user.id)

        
        payments_sent_list = Payment.objects.filter(
                account__customer__user_id=request.user.id)

        last_payment_received = transaction_list.last()

        last_payment_sent = payments_sent_list.last()

        customers = Customer.objects.all()
        accounts = Account.objects.all()

        login_user_accounts = Account.objects.filter(
            customer_id=request.user.id)
        login_customer = Customer.objects.filter(id=request.user.id)

        all_deposits = sum(
            transaction.amount for transaction in transaction_list)
        all_withdrawals = sum(
            transaction.amount for transaction in payments_sent_list)

        balance = (all_deposits - all_withdrawals)

        self.context['all_deposits'] = all_deposits
        self.context['all_withdrawals'] = all_withdrawals
        self.context['transaction_list'] = transaction_list
        self.context['payments_sent_list'] = payments_sent_list
        self.context['last_payment_received'] = last_payment_received
        self.context['last_payment_sent'] = last_payment_sent
        self.context['balance'] = balance
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
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        transaction_list = PostTransaction.objects.filter(
            account__customer__user_id=request.user.id).order_by("date")

        createhistory_list = CreateHistory.objects.filter(
            account__customer__user_id=request.user.id).order_by("date")

        debit_createhistory_list = createhistory_list.filter(account__customer__user_id=request.user.id,
                                                             top_up_type='Debit').order_by("date")
        credit_createhistory_list = createhistory_list.filter(account__customer__user_id=request.user.id,
                                                              top_up_type='Credit').order_by("date")

        if request.user:
            payments_sent_list = Payment.objects.filter(
                account__id=request.user.id).order_by("-date")

        transaction_data = {'Date': [],
                            'Account Name': [], 'Credit': [], 'Debit': []}

        for transaction in transaction_list:
            transaction_data['Date'].append(transaction.date)
            transaction_data['Account Name'].append(
                transaction.company_name)

            transaction_data['Credit'].append('$'+str(transaction.amount))
            transaction_data['Debit'].append('---')

        for transaction in credit_createhistory_list:
            transaction_data['Date'].append(transaction.date)
            transaction_data['Account Name'].append(
                transaction.company_name)
            transaction_data['Credit'].append('$'+str(transaction.amount))
            transaction_data['Debit'].append('---')

        for transaction in payments_sent_list:
            transaction_data['Date'].append(transaction.date)
            transaction_data['Account Name'].append(transaction.account_name)
            transaction_data['Credit'].append('---')
            transaction_data['Debit'].append('-$' + str(transaction.amount))

        for transaction in debit_createhistory_list:
            transaction_data['Date'].append(transaction.date)
            transaction_data['Account Name'].append(transaction.company_name)
            transaction_data['Credit'].append('---')
            transaction_data['Debit'].append('-$'+str(transaction.amount))

        transaction_dataframe = pd.DataFrame.from_dict(transaction_data)
        transaction_dataframe['Date'] = pd.to_datetime(
            transaction_dataframe.Date)
        transaction_dataframe['Date'] = transaction_dataframe['Date'].dt.date
        transaction_dataframe.style.format(
            {"Date": lambda t: t.strftime("%m/%d/%Y")})
        transaction_dataframe.sort_values(by='Date', ascending=False)

        customers = Customer.objects.all()
        accounts = Account.objects.all()

        login_user_accounts = Account.objects.filter(
            id=request.user.id)
        login_customer = Customer.objects.filter(id=request.user.id)

        all_deposits = sum(
            transaction.amount for transaction in transaction_list)
        all_withdrawals = sum(
            transaction.amount for transaction in payments_sent_list)

        self.context['transaction_dataframe'] = transaction_dataframe
        return render(request, self.template_name, self.context)
