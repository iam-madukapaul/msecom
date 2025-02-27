from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItems, Order, BillingAddress, Coupon
from .forms import CheckoutForm, CouponForm
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View

# Create your views here.
def index(request):
    items = Item.objects.all()
    page = request.GET.get('page', 1)
    
    paginator = Paginator(items, 4)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {
        'items': items,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        context = {
            'order': order,
        }
        return render(request, 'order_summary.html', context)
    except ObjectDoesNotExist:
        messages.error(request, 'You do not have an active order')
        return redirect('index')

@login_required(login_url='login')
def checkout(request):
    form = CheckoutForm()
    order = Order.objects.get(user=request.user, ordered=False)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                street_adress = form.cleaned_data.get('street_adress')
                apartment_adress = form.cleaned_data.get('apartment_adress')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                #TODO: Add functionality to these fields later on.
                # same_billing_address = form.cleaned_data.get('same_billing_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=request.user,
                    street_adress=street_adress,
                    apartment_adress=apartment_adress,
                    country=country,
                    state=state,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                #TODO: Add a redirect to the selected payment option
                return redirect('checkout')
            else:
                messages.warning(request, "Failed checkout.")
                return redirect('checkout')

        except ObjectDoesNotExist:
            messages.warning(request, 'You do not have an active order')
            return redirect('order-summary')
    context = {
                'form': form,
                'order': order,
                'CouponForm': CouponForm,
                'DISPLAY_COUPON_FORM': True,
            }
    return render(request, 'checkout.html', context)


@method_decorator(login_required(login_url='login'), name='dispatch')
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
            }
            return render(self.request, 'payment.html', context)
        else:
            messages.warning(self.request, 'You have not added a billing address')
            return redirect('checkout')

def detail_product(request, slug):
    item = get_object_or_404(Item, slug=slug)
    context = {
        'item': item,
    }
    return render(request, 'productpage.html', context)


@login_required(login_url='login')
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItems.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        # Check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            # Display a message saying the item is already in the cart
            messages.info(request, 'This item is already in your cart.')
        else:
            # Add the item to the order
            order.item.add(order_item)
            messages.info(request, 'This item was added to your cart.')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, 'This item was added to your cart.')

    return redirect('product', slug=slug)

# @login_required(login_url='login')
# def add_to_cart(request, slug):
#     item = get_object_or_404(Item, slug=slug)
#     order_item, created = OrderItems.objects.get_or_create(item=item, user=request.user, ordered=False)
#     order_qs = Order.objects.filter(user=request.user, ordered=False) # we are getting orders that has not been completed
#     # we need to check if the order_qs exist
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.item.filter(item__slug=item.slug).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, 'This item quantity was updated.')
#             return redirect('product', slug=slug)
#         else:
#             order.item.add(order_item)
#             messages.info(request, 'This item was added to your cart.')
#             return redirect('product', slug=slug)
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(user=request.user, ordered_date=ordered_date)
#         order.item.add(order_item)
#         messages.info(request, 'This item was added to your cart.')
#         return redirect('product', slug=slug)

@login_required(login_url='login')
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False) # we are getting orders that has not been completed
    # we need to check if the order_qs exist
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItems.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.item.remove(order_item)
            messages.info(request, 'This item was removed to your cart.')
            return redirect('product', slug=slug)
        else:
            messages.info(request, 'This item is not in your cart.')
            return redirect('product', slug=slug)
    else:
        # add a message saying the user doesnt have an order
        messages.info(request, 'You do not have an active order.')
        return redirect('product', slug=slug)
    

@login_required(login_url='login')
def add_single_item_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItems.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False) # we are getting orders that has not been completed
    # we need to check if the order_qs exist
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'An item has been incremented.')
            return redirect('order-summary')
        else:
            order.item.add(order_item)
            messages.info(request, 'This item was added to your cart.')
            return redirect('order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.item.add(order_item)
        messages.info(request, 'This item was added to your cart.')
        return redirect('order-summary')

    
@login_required(login_url='login')
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False) # we are getting orders that has not been completed
    # we need to check if the order_qs exist
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItems.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.remove(order_item)
            messages.info(request, 'An item has been deducted.')
            return redirect('order-summary')
        else:
            messages.info(request, 'This item is not in your cart.')
            return redirect('product', slug=slug)
    else:
        # add a message saying the user doesnt have an order
        messages.info(request, 'You do not have an active order.')
        return redirect('product', slug=slug)
    

@login_required(login_url='login')
def delete_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False) # we are getting orders that has not been completed
    # we need to check if the order_qs exist
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.item.filter(item__slug=item.slug).exists():
            order_item = OrderItems.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.item.remove(order_item)
            messages.info(request, 'An item has been deleted from cart.')
            return redirect('order-summary')
        else:
            messages.info(request, 'This item is not in your cart.')
            return redirect('product', slug=slug)
    else:
        # add a message saying the user doesnt have an order
        messages.info(request, 'You do not have an active order.')
        return redirect('product', slug=slug)
    
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon does not exist.')
        return redirect('checkout')

class AddCouponView(View):
    def post(self, *args, **kwargs):
            form = CouponForm(self.request.POST or None)
            if form.is_valid():
                # note we did not go deep, no validation on how many times this coupon has been used or if you have use this coupon before.
                try:
                    code = form.cleaned_data.get('code')
                    order = Order.objects.get(user=self.request.user, ordered=False) 
                    order.coupon = get_coupon(self.request, code)
                    order.save()
                    messages.success(self.request, 'Successfully added coupon.')
                    return redirect('checkout')

                except ObjectDoesNotExist:
                    messages.info(self.request, 'You do not have an active order.')
                    return redirect('checkout')
        
        
        