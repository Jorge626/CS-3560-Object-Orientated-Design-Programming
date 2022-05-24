from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    customerID = models.BigAutoField(primary_key=True)
    # fname = models.CharField(max_length=50)
    fullName = models.CharField(max_length=50, default="uknown")
    phoneNumber = models.CharField(max_length=15)

    def __str__(self):
        return str(self.user)


class Account(models.Model):
    accountID = models.BigAutoField(
        primary_key=True)
    customerID = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    serviceDate = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    serviceAddress = models.CharField(max_length=200)
    serviceAddress2 = models.CharField(
        max_length=200, null=True)  # new field
    city = models.CharField(max_length=200, null=True)  # new field
    state = models.CharField(max_length=2, null=True)  # new field
    zipcode = models.CharField(max_length=5, null=True)  # new field
    suspend = models.BooleanField(default=False)
    suspendDate = models.DateTimeField(
        null=True, blank=True)  # auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.accountID)


class Address(models.Model):
    addressID = models.BigAutoField(
        primary_key=True)
    customerID = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=40)

    def __str__(self):
        return self.address


class Rate(models.Model):
    tierID = models.BigAutoField(
        primary_key=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    theRange = models.CharField(max_length=21)

    def __str__(self):
        return str(self.tierID)


class Bill(models.Model):
    billID = models.BigAutoField(
        primary_key=True)
    accountID = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True)
    tierID = models.ForeignKey(
        Rate, on_delete=models.CASCADE, null=True, blank=True)
    amountDue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True)
    currentReading = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    readingDate = models.DateField(null=True, blank=True)
    lateFee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paidInFull = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return str(self.billID)


    def get_dueDate(self):
        dueDate = self.readingDate + datetime.timedelta(days=30)
        return dueDate
