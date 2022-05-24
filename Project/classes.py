# Classes to be used in the Oracle Water Billing System

# This class will keep track of the meter readings for each customer
class Account:
    def __init__(self, account_id, customer_id, service_date, service_address, suspend, suspend_date, comment):
        self.accountID = account_id
        self.customerID = customer_id
        self.serviceDate = service_date
        self.serviceAddress = service_address
        self.suspend = suspend
        self.suspendDate = suspend_date
        self.comment = comment

    # This method will return the meter details
    def get_meter_details(self):
        pass

    # This method will allow the user to set the meter details
    def set_meter_details(self):
        pass

    # This method will help compute the usage of the customer based on the meter details
    def compute_usage(self):
        pass


# This class will keep track of the billing information for customers
class Bill:
    def __init__(self, bill_id, account_id, amount_due, due_date, previous_reading, current_reading, reading_date,
                 late_fee, paid_in_full):
        self.billID = bill_id
        self.accountID = account_id
        self.amountDue = amount_due
        self.dueDate = due_date
        self.currentReading = current_reading
        self.readingDate = reading_date
        self.lateFee = late_fee
        self.paidInFull = paid_in_full

    # This method will return the billing details
    def get_bill(self):
        pass

    # This method will allow the user to set the billing details
    def set_bill(self):
        pass

    # This method will create the bill for the customer
    def generate_bill(self):
        pass

    # This method will send the bill to the customer
    def send_bill(self):
        pass


# This class will set the billing rates for the customers based upon their meter readings
class Rates:
    def __init__(self, tier_id, usage_range, price):
        self.tierID = tier_id
        self.usageRange = usage_range
        self.price = price

    # This method will return the rate
    def get_rate(self):
        pass

    # This method will allow the user to set the rate
    def set_rate(self):
        pass
