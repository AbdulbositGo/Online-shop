from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        coupon = Coupon.objects.filter(
            code__iexact=code,
            valid_from__lte=now,
            valid_to__gte=now
        ).first()
        if coupon:
            request.session['coupon_id'] = coupon.id
        else:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
