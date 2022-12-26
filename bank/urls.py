from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic.base import RedirectView

from . import views

app_name = 'bank'
# from bank.account.register_view import (
#     ActivateView,
#     AccountActivationSentView,
#     UserRegisterView,
# )
# from bank.account.logout_view import UserLogoutView
# from bank.account.login_view import UserLoginView


urlpatterns = [
    path('customer/account_suspended',
         views.SuspendAccount.as_view(), name='suspend_account'),
     path(
          route="my_dashboard",
          view=views.DashboardHomeView.as_view(),
          name="dashboard_home"
     ),
     path(
          route="customer-portal",
          view=views.CustomerDashView.as_view(),
          name="customerdash_home"
     ),
     path(
          route="customer/transaction_history",
          view=views.TransactionHistoryView.as_view(),
          name="transaction_history"
     ),
    path(
        route="customer/transaction_successful",
        view=views.TransactionSuccessful.as_view(),
        name="transaction_success"
    ),
    path('customer/create/', views.CustomerCreate.as_view(), name='customer-create'),
    path('enrol-customer/create/', views.EnrolCustomerCreate.as_view(), name='enrol-customer-create'),
    path('customer/<int:pk>/update/',
         views.CustomerUpdate.as_view(), name='customer-update'),

    path('customer/<int:pk>/delete/',
         views.CustomerDelete.as_view(), name='customer-delete'),

    path('customer-user/<int:pk>/update/',
         views.CustomerUserUpdate.as_view(), name='customer-user-update'),

    path('customer/<int:pk>',
         views.CustomerDetailView.as_view(), name='customer-detail'),

    path('<int:pk>/customers',
         views.CustomerListView.as_view(), name='customers-list'),

    path('user/create/', views.UserCreate.as_view(), name='user-create'),
    path('user/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    path('user/<int:pk>/delete/',
         views.UserDelete.as_view(), name='user-delete'),

    path('enrol-account/create/', views.EnrolAccountCreate.as_view(),
         name='enrol-account-create'),
    path('account/create/', views.AccountCreate.as_view(), name='account-create'),
    path('account/<int:pk>/update/',
         views.AccountUpdate.as_view(), name='account-update'),
    path('account/<int:pk>/delete/',
         views.AccountDelete.as_view(), name='account-delete'),

    path('account/<int:pk>',
         views.AccountDetailView.as_view(), name='account-detail'),

    path('<int:pk>/accounts',
         views.AccountListView.as_view(), name='accounts-list'),

    path('posttransaction/create/', views.PostTransactionCreate.as_view(),
         name='posttransaction-create'),
    path('posttransaction/<int:pk>/update/',
         views.PostTransactionUpdate.as_view(), name='posttransaction-update'),
    path('posttransaction/<int:pk>/delete/',
         views.PostTransactionDelete.as_view(), name='posttransaction-delete'),

    path('posttransaction/<int:pk>',
         views.PostTransactionDetailView.as_view(), name='posttransaction-detail'),

    path('<int:pk>/posttransactions',
         views.PostTransactionListView.as_view(), name='posttransactions-list'),

    path('transactionhistory/create/', views.TransactionHistoryCreate.as_view(),
         name='transactionhistory-create'),

    path('payment/create/', views.PaymentCreate.as_view(),
         name='payment-create'),
     path('customer/payment/send/', views.CustomerPaymentCreate.as_view(),
         name='customer-payment-create'),
    path('payment/<int:pk>/update/',
         views.PaymentUpdate.as_view(), name='payment-update'),
    path('payment/<int:pk>/delete/',
         views.PaymentDelete.as_view(), name='payment-delete'),

    path('<int:pk>/payments',
         views.PaymentListView.as_view(), name='payment-list'),

    
#     path(
#         route="user/paid/",
#         view=views.ReceivedTransactionsView.as_view(),
#         name="received_transaction"
#     ),
#     path(
#         route="user/sent/",
#         view=views.SentTransactionsView.as_view(),
#         name="sent_transaction"
#     ),
    path(
        route='user/details/',
        view=views.CustomerProfileView.as_view(),
        name='user_profile_details'
    ),
    path(
        route="user/accounts/",
        view=views.AccountListView.as_view(),
        name="list_accounts"
    ),

    # ACCOUNT URLS #

    # account/login/
    path(
        route='',
        view=views.UserLoginView.as_view(),
        name='login'
    ),

    # account/login/
    path(
        route='account/register',
        view=views.UserRegisterView.as_view(),
        name='register'
    ),

    # account/logout/
    path(
        route='accounts/logged_out',
        view=views.UserLogoutView.as_view(),
        name='log-out'
    ),

    path(route='account_activation_sent/',
         view=views.AccountActivationSentView.as_view(),
         name='account_activation_sent'
         ),

    path(route='activate/<uidb64>/<token>/',
         view=views.ActivateView.as_view(),
         name='activate'
         ),
]
