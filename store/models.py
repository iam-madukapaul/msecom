from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# Create your models here.
LABEL_CHOICES = (
    ('PR', 'primary'),
    ('SE', 'secondary'),
    ('DA', 'danger'),
    ('DK', 'dark'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    item_image = models.ImageField(upload_to='img', default='default.jpg')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.title 

class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    
    #To show amount saved on this item, if there is a discount price
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    item = models.ManyToManyField(OrderItems)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    

    '''
    1.) Item added to cart
    2.) Adding a billing address
        (failed checkout)
    3.) Payment
        (preprocessing, processing, packaging, etc...)
    4.) Being delivered (keeping track of the order)
    5.) delivered (when it has been recieved)
    6.) Refunds (keep track of the number of refunds)
    '''

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.item.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_adress = models.CharField(max_length=100)
    apartment_adress = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    def __str__(self):
        return self.code
    