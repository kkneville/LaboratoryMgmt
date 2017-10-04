from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from models import *
import random, re, datetime
from datetime import datetime
from django.db import models
from ..login.models import Member


def current_member(request):
    id = request.session['id']
    member = Member.objects.get(id=id)
    return member

def logout(request):
    request.session.pop('id')
    return redirect(reverse('index'))

def dashboard(request):
    member = current_member(request)

    context = {
    	"member": member,
    }
    return render(request, "lab/dashboard.html", context)

def add(request):
    member = current_member(request)
    if "errors" in request.session :
        errors = request.session['errors']
        request.session.pop('errors')
    else:
        errors = []
    context = {
        "member": member,
        "errors": errors,
    }
    return render(request, "belt3/add.html", context)
