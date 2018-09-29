# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse , HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
import base64
from datetime import datetime , timedelta
from time import time
import uuid
from mysite import models

# Create your views here.

def home(request):
    try:
        account = request.session['account']
        picture = models.Picture.objects.filter(uploader_id=account)
    except:
        pass
    template = get_template('home.html')
    html = template.render(locals())
    return HttpResponse(html)

def login(request):
    if request.method == 'POST':
        login_account = request.POST.get('account')
        login_password = request.POST.get('password')
        try:
            account = models.Account.objects.get(account=login_account)
            if account.password == login_password:
                if account.verify != None:
                    return HttpResponse('please verify')
                request.session['account'] = account.account
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Wrong password')
        except:
            return HttpResponse('Account not exist')
    template = get_template('login.html')
    html = template.render(locals())
    return HttpResponse(html)

def logout(request, coi=''):
    del request.session['account']
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        new_account = request.POST.get('account')
        new_password = request.POST.get('password')
        new_email = request.POST.get('email')
        if new_account == None or new_password == None or new_account == '' or new_password == '':
            return HttpResponse('Wrong account or password')
        try:
            models.Account.objects.get(account=new_account)
            return HttpResponse('Account exist')
        except:
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [new_email,]
            subject = 'Thank you for registering to our site'
            message = 'http://140.116.138.69:8001/verify/' + base64.b64encode( new_account.rjust( 20 , ' ' ) + str( time() ) )
            send_mail( subject, message, email_from, recipient_list )
            save_account = models.Account.objects.create(account=new_account, password=new_password, verify=message)
            save_account.save()
            return HttpResponseRedirect('/')
    template = get_template('register.html')
    html = template.render(locals())
    return HttpResponse(html)

def verify(request, v):
    v = base64.b64decode( v )
    account = v[:20].strip()
    register_time = datetime.fromtimestamp( float(v[20:]) )
    if register_time + timedelta(days=1) >= datetime.now():
        models.Account.objects.filter(account=account).update(verify=None)
        return HttpResponse('verify success')
    else:
        return HttpResponse('out of the date')

def upload(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        account = request.session['account']
        img = request.FILES['picture']
        img.name = account + '_' + name + '_' + uuid.uuid4().hex + '.' + img.name.split('.')[-1]
        picture = models.Picture.objects.create(name=name, description=description, uploader_id=account, picture=img)
        picture.save()       
    return HttpResponseRedirect('/')