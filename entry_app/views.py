
# from twilio.rest import Client

import requests
import json
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader
from entry_app.forms import HostForm, VisitorForm, Checkout
from entry_app.models import Visitor,Host


# account_sid = 'AaaC4fae24bda331fbeae76ceefc021cbb0066' # Found on Twilio Console Dashboard
# auth_token = '8d95bfe44d93f2557783f691f2c9b367' # Found on Twilio Console Dashboard
#
# myPhone = '+918299698057' # Phone number you used to verify your Twilio account
# TwilioNumber = '+19513632557' # Phone number given to you by Twilio


URL = 'https://www.way2sms.com/api/v1/sendCampaign'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)

# get response
"""
  Note:-
    you must provide apikey, secretkey, usetype, mobile, senderid and message values
    and then requst to api
"""
# print response if you want

def index(request):
    template = loader.get_template('index.html')
    context = {
        'v_all' : Visitor.objects.all(),
        'a_host' : Host.objects.last(),
    }
    return HttpResponse(template.render(context, request))
def hosts_form(request):
    template = loader.get_template('hform.html')
    form_object = HostForm()
    if request.method == 'POST':
        form_object = HostForm(request.POST)
        if form_object.is_valid():
            entered_name = form_object.cleaned_data['name']
            entered_email = form_object.cleaned_data['email']
            entered_phone = form_object.cleaned_data['phone']
            Host.objects.get_or_create(name=entered_name, email=entered_email, phone=entered_phone)
            return index(request)
    context = {
        'form_full': form_object
    }
    return HttpResponse(template.render(context, request))

def visitor_form(request):
    # client = Client(account_sid, auth_token)

    template = loader.get_template('vform.html')
    form_object = VisitorForm()
    if request.method == 'POST':
        form_object = VisitorForm(request.POST)
        if form_object.is_valid():
            entered_name = form_object.cleaned_data['name']
            entered_email = form_object.cleaned_data['email']
            entered_phone = form_object.cleaned_data['phone']
            current_host=Host.objects.last()
            Visitor.objects.get_or_create(name=entered_name, email=entered_email, phone=entered_phone,hostname=current_host.name)
            last_val=Visitor.objects.last()
            message='\nName : '+str(entered_name)+'\n Email : '+str(entered_email)+'\n Phone : '+str(entered_phone)+'\n Checkin : '+str(last_val.check_in)
            send_mail(subject="Visitor Entry Details",from_email=settings.EMAIL_HOST_USER,message=message,recipient_list=[current_host.email,'entry.manage.satbir@gmail.com'],auth_password=settings.EMAIL_HOST_PASSWORD)
            sendPostRequest(URL, 'TK9Y5G8ZV55PHF1XE9ZGUTVLWFRK7CMK', 'WBOCI915B7I9EDU9', 'stage', current_host.phone,
                                       'entry', message)

            return index(request)
    context = {
        'form_full': form_object
    }
    return HttpResponse(template.render(context, request))

def visitor_checkout(request):
    template = loader.get_template('checkout.html')
    form_object = Checkout()
    if request.method == 'POST':
        form_object = Checkout(request.POST)
        if form_object.is_valid():
            entered_phone = form_object.cleaned_data['phone']
            Visitor.objects.filter(phone=entered_phone).update(phone=entered_phone)
            visitor_co = Visitor.objects.get(phone=entered_phone)
            message='\nName : '+str(visitor_co.name)+'\n Email : '+str(visitor_co.email)+'\n Phone : '+str(entered_phone)+'\n Checkin : '+str(visitor_co.check_in)+'\n Checkout : '+str(visitor_co.check_out)+'\n Host : '+str(visitor_co.hostname)
            send_mail(subject="Visitor Entry Details", from_email=settings.EMAIL_HOST_USER, message=message,
                      recipient_list=[visitor_co.email, 'entry.manage.satbir@gmail.com'],
                      auth_password=settings.EMAIL_HOST_PASSWORD)
            return index(request)
    context = {
        'form_full': form_object
    }
    return HttpResponse(template.render(context, request))