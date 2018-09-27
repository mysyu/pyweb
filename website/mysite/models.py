# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Account(models.Model):
    account = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    verify = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        db_table = 'Account'