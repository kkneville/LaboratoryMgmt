from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from models import *
import random, re
from django.db import models
from ..logreg.models import User


def current_user(request):
    id = request.session['id']
    return User.objects.get(id=id)

def logout(request):
    request.session.pop('id')
    return redirect(reverse('/'))

def index(request):
    if "id" in request.session:
        user = current_user(request)
    people = User.objects.all()
    context = {
        "user": user,
        "people": people,
    }
    return render(request, "manager/index.html", context)

def showuser(request, id):
    user = current_user(request)
    person = User.objects.get(id=id)
    quotes = Quote.objects.filter(liked_by__id=id)[:3]
    posts = Quote.objects.filter(posted_by__id=id)[:2]
    print user.level
    context = {
        "user": user,
        "person": person,
        "quotes": quotes,
        "posts": posts,
    }
    return render(request, "manager/showuser.html", context)

def edituser(request, id):
    if "errors" in request.session :
        errors = request.session['errors']
    else :
        errors = []
    user = current_user(request)
    person = User.objects.get(id=id)
    context = {
        "person": person,
        "user": user,
        "errors": errors,
    }
    request.session.pop("errors")
    return render(request, "manager/edit.html", context)

def deletecheck(request, id):
    person = User.objects.get(id=id)
    context = {
        "person": person,
    }
    return render(request, "manager/deletecheck.html", context)
