import stripe
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render,redirect, get_object_or_404 

from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_KEY


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:complated'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))

        session_data = {
            "mode": 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, status=303)
    else:
        print(locals())
        return render(request, 'payment/process.html', locals())

    