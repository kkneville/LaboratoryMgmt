from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from models import *
import random, re
import bcrypt


def index(request):
    if "errors" not in request.session:
        request.session['errors'] = []
    context = {
        "errors": request.session['errors'],
    }
    request.session.pop("errors")
    return render(request, "logreg/login.html", context)

def register(request):
    if "errors" not in request.session:
        request.session['errors'] = []
    context = {
        "errors": request.session['errors'],
    }
    request.session.pop("errors")
    return render(request, "logreg/register.html", context)

def adminadd(request):
    if "errors" not in request.session:
        request.session['errors'] = []
    context = {
        "errors": request.session['errors'],
    }
    request.session.pop("errors")
    return render(request, "logreg/adminadd.html", context)

def adduser(request):
    if request.method == "POST":
        errors = User.objects.validate_reg(request.POST)
        if errors:
            request.session['errors'] = errors
            return redirect("/index")
        user = User.objects.create_user(request.POST)
        request.session['id'] = user.id
    return redirect(reverse("dashboard"))

def edit(request):
    id=request.POST['id']
    if request.method == "POST":
        errors = User.objects.validate_edit(request.POST)
        if errors:
            request.session['errors'] = errors
            return redirect(reverse('edituser', kwargs = {'id':id}))
    person = User.objects.edit_user(request.POST)
    return redirect(reverse('showuser', kwargs = {'id':id}))

def delete(request):
    id=request.POST['id']
    person = User.objects.get(id=id)
    person.delete()
    return redirect(reverse("showusers"))


def login(request):
    if request.method == "POST":
        result = User.objects.validate_login(request.POST)
        if len(result['errors']) > 0 :
            request.session['errors'] = result['errors']
            return redirect("/index")
        else :
            user = result['user']
            request.session['id'] = user.id
        return redirect(reverse("dashboard"))

def logout(request):
    if "id" in request.session:
        request.session.pop('id')
    return redirect('/index')
