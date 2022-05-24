from collections import UserList
from django.db.models.fields import DateField
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.base import TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import connection
from .models import Bill, Account, Customer, Address, Rate, User
from .forms import AccountForm, UsageForm, SuspensionForm, RateForm
from .functions import *
from django.utils import timezone
from django.contrib.auth import get_user_model
import datetime
date = datetime.datetime.now().date()
search = False

user = get_user_model()


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        if not self.request.user.groups.filter(name="Clerk").exists():
            return reverse_lazy('bill')
        else:
            return reverse_lazy('homepage')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('homepage')
        return super(RegisterPage, self).get(*args, **kwargs)


def bill_detail_view(request):
    obj = Bill.objects.get(accountID=1)

    H1_STRING = f"""
    <h1>{bill_obj.amountDue}!</h1>
    """
    P_STRING = f"""
    <p>{bill_obj.currentReading}!</p>
    """
    HTML_STRING = H1_STRING + P_STRING

    return HttpResponse(HTML_STRING)


class ViewBillPage(LoginRequiredMixin, ListView):
    template_name = 'base/view_Bill.html'
    context_object_name = 'latest_paid_bills'

    def get_queryset(self):
        queryset = {
            'unpaid_Bills': Bill.objects.filter(paidInFull=False).order_by('-readingDate')[0:1],
            'paid_Bills': Bill.objects.filter(paidInFull=True).order_by('-readingDate')[0:5]
        }
        return queryset


class BillPage(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = 'bill/detail.html'


class suspensionForm(LoginRequiredMixin, ListView):
    model = Bill
    template_name = 'base/suspension.html'


class usageForm(LoginRequiredMixin, ListView):
    template_name = 'base/usage.html'


class homePage(LoginRequiredMixin, ListView, AccessMixin):
    model = Account
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        return context


def add_account(request):

    submitted = False  # Variable to check if form was submitted, initially not submitted
    if request.method == "POST":  # If we are posting
        # Then take what they posted and pass it into AccountForm
        form = AccountForm(request.POST)
        if form.is_valid():  # Check if the form is valid
            form.save()  # And Save it to the database
            # Then return back to page WITH submitted set to True
            return HttpResponseRedirect('/add_account?submitted=True')
    else:
        form = AccountForm
        # If submitted then it will be in the GET request, meaning they submitted the form.
        if 'submitted' in request.GET:
            submitted = True

    # -------------------------------------------------------------------------------------------
    # Takes in the user input from the HTML url and assigns it to the 'customer variable' for searching
    # the database using that customer ID
    if 'customer' in request.GET:
        search = True
        customer = request.GET
        customer = list(customer.values())[0]

        cursor = connection.cursor()
        cursor.execute("""
        SELECT
            base_customer.fullName,
            base_customer.phoneNumber,
            base_customer.customerID,
            auth_user.email
        From base_customer Inner Join
            auth_user On base_customer.user_id = auth_user.id
        Where
            base_customer.customerID = """ + customer)
        row = dictfetchall(cursor)
        return render(request, 'base/add_account.html', {'form': form, 'submitted': submitted, 'customer_info': row, 'search': search})
    # -------------------------------------------------------------------------------------------
    # Passed in the form and submitted: which will be True or False
    return render(request, 'base/add_account.html', {'form': form, 'submitted': submitted})

    form = AccountForm
    return render(request, 'base/add_account.html', {'form': form})


def usage(request):
    global customer
    submitted = False  # Variable to check if form was submitted, initially not submitted
    if request.method == "POST":  # If we are posting
        # Then take what they posted and pass it into AccountForm
        form = UsageForm(request.POST)
        if form.is_valid():  # Check if the form is valid
            form.save()  # And Save it to the database
            # Then return back to page WITH submitted set to True
            return HttpResponseRedirect('/usage?submitted=True')
    else:
        form = UsageForm
        # If submitted then it will be in the GET request, meaning they submitted the form.
        if 'submitted' in request.GET:
            submitted = True
    # Passed in the form and submitted: which will be True or False

    # -------------------------------------------------------------------------------------------
    # Takes in the user input from the HTML url and assigns it to the 'customer variable' for searching
    # the database using that account ID
    if 'customer' in request.GET:
        search = True
        customer = request.GET
        customer = list(customer.values())[0]

        cursor = connection.cursor()
        cursor.execute("""
        SELECT
            base_customer.fullName,
            base_customer.phoneNumber,
            base_customer.customerID,
            base_account.accountID,
            auth_user.email
        From
            base_customer Inner Join
            auth_user On base_customer.user_id = auth_user.id Inner Join
            base_account On base_customer.customerID = base_account.customerID_id
        Where
            base_account.accountID = """ + customer)  # customer = input in search box
        row = dictfetchall(cursor)
        return render(request, 'base/usage.html', {'form': form, 'submitted': submitted, 'customer_info': row, 'search': search})
    # -------------------------------------------------------------------------------------------

    if(submitted == True):
        updateBills(customer)

    return render(request, 'base/usage.html', {'form': form, 'submitted': submitted})

    form = UsageForm
    return render(request, 'base/usage.html', {'form': form})


def update_account(request):
    global customer
    submitted = False
    #form = SuspensionForm
    # -------------------------------------------------------------------------------------------
    # Takes in the user input from the HTML url and assigns it to the 'customer variable' for searching
    # the database using that account ID
    if 'customer' in request.GET:
        search = True
        customer = request.GET
        customer = list(customer.values())[0]

        suspend = Account.objects.get(accountID=customer)
        form = SuspensionForm(instance=suspend)

        cursor = connection.cursor()
        cursor.execute("""
        SELECT
            base_customer.fullName,
            base_customer.phoneNumber,
            base_customer.customerID,
            auth_user.email,
            base_account.accountID
        From
            base_customer Inner Join
            auth_user On base_customer.user_id = auth_user.id Inner Join
            base_account On base_customer.customerID = base_account.customerID_id
        Where
            base_account.accountID = """ + customer)  # customer = input in search box
        row = dictfetchall(cursor)

        if request.method == 'POST':
            form = SuspensionForm(request.POST, instance=suspend)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/suspension?submitted=True')

        return render(request, 'base/suspension.html', {'form': form, 'submitted': submitted, 'customer_info': row, 'search': search})
    else:
        form = SuspensionForm
        # If submitted then it will be in the GET request, meaning they submitted the form.
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'base/suspension.html', {'form': form, 'submitted': submitted})

    form = SuspensionForm
    return render(request, 'base/suspension.html', {'form': form})


def rates(request):
    submitted = False
    # -------------------------------------------------------------------------------------------
    # Takes in the user input from the HTML url and assigns it to the 'customer variable' for searching
    # the database using that account ID
    if 'tierNum' in request.GET:
        search = True
        tierNum = request.GET
        tierNum = list(tierNum.values())[0]

        suspend = Rate.objects.get(tierID=tierNum)
        form = RateForm(instance=suspend)

        cursor = connection.cursor()
        cursor.execute("""
        SELECT
            base_rate.tierID,
            base_rate.price,
            base_rate.theRange
        From base_rate 
        Where
            base_rate.tierID = """ + tierNum)  # customer = input in search box
        row = dictfetchall(cursor)

        if request.method == 'POST':
            form = RateForm(request.POST, instance=suspend)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/rates?submitted=True')

        return render(request, 'base/rates.html', {'form': form, 'submitted': submitted, 'tierNum_info': row, 'search': search})
    else:
        form = RateForm
        # If submitted then it will be in the GET request, meaning they submitted the form.
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'base/rates.html', {'form': form, 'submitted': submitted})


class AccountList(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'base/account_list.html'
    #user_bills = Bill.objects.filter(user=request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.filter(
            user=self.request.user.pk)
        context['accounts'] = Account.objects.filter(
            customerID=self.request.user.customer.customerID)
        return context


class BillList(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'base/bill_list.html'

    def get_context_data(self, **kwargs):
        context = super(BillList, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.filter(pk=71)
        context['bills'] = Bill.objects.filter(
            accountID=71).order_by('-readingDate')
        return context


'''
def billList(request):
    global customer

    clicked = False
    if 'customer' in request.GET:
        customer = request.GET
        customer = list(customer.values())[0]
        clicked = True

        cursor = connection.cursor()
        cursor.execute("""
        SELECT
            base_customer.fullName,
            base_customer.phoneNumber,
            base_customer.customerID,
            base_account.accountID,
            auth_user.email
            base_bil.billID
        From
            base_customer Inner Join
            auth_user On base_customer.user_id = auth_user.id Inner Join
            base_account On base_customer.customerID = base_account.customerID_id Inner Join
            base_bill On base_account.accountID = base_bill.accountID_id
        Where
            base_account.accountID = """ + customer)  # customer = input in search box
        row = dictfetchall(cursor)
        return render(request, 'base/account_list.html', {'customer_info': row, 'clicked': clicked})

    return render(request, 'base/account_list.html', {'clicked': clicked})
'''
