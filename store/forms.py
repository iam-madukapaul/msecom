from django import forms
from django_countries.fields import CountryField

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)

class CheckoutForm(forms.Form):
    street_adress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '1234 Main St'}))
    apartment_adress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apartment or suite'}), required=False)
    country = CountryField(blank_label="(select country)").formfield()
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Promo code','aria-label': 'Promo code','aria-describedby': 'button-addon2'}))
    
    

