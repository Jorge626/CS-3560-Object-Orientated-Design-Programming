from django.urls import path

from .views import CustomLoginView, RegisterPage, ViewBillPage, homePage, BillPage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LogoutView
from base.views import bill_detail_view, AccountList, BillList
from . import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    #path('login_success/', views.login_success, name='login_success'),
    path('bills/<int:pk>/', BillPage.as_view(), name='detail'),
    path('bills/', ViewBillPage.as_view(), name='view_Bill'),
    path('add_account/', views.add_account, name='add-account'),
    path('usage/', views.usage, name='usage'),
    path('suspension/', views.update_account, name='suspension'),
    path('suspension/<str:pk>/', views.update_account, name='suspension'),
    path('rates/', views.rates, name='rates'),
    path('', homePage.as_view(), name='homepage'),

    path('mybills/', BillList.as_view(), name='bill')
]

urlpatterns += staticfiles_urlpatterns()
