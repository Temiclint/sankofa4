import os
import json
import datetime
from django import template
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.utils import timezone
from crm.models import *



register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value.file.name)


# Checking for group filter
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.simple_tag
def total_invoices():
    return Invoice.objects.all().count()

@register.simple_tag
def total_quotes():
    return Estimate.objects.all().count()

@register.simple_tag
def total_revenue():
    total = Invoice.objects.all().aggregate(Sum('grand_total'))['grand_total__sum']
    if total:
        return int(total)
    else:
        return 0

@register.simple_tag
def total_clients():
    return Contact.objects.filter(role=3).count()

@register.simple_tag
def quote_invoice_ratio():
    invoice_count = Invoice.objects.all().count()
    quote_count = Estimate.objects.all().count()
    data = [quote_count, invoice_count]
    ratio = json.dumps(data)
    return ratio