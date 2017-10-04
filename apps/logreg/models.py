from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import random, re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validate_reg(self, formdata):
        errors = []
        if len(formdata['firstname']) < 1 :
            errors.append("First name is required.")
        if len(formdata['lastname'])  < 1 :
            errors.append("Last name is required.")
        if len(formdata['email'])  < 1 :
            errors.append("Email is required.")
        if len(formdata['password'])  < 1 :
            errors.append("Password is required.")
        if formdata['password'] != formdata['passwordconfirm'] :
            errors.append("Passwords must match.")
        return errors

    def validate_login(self, formdata):
        errors = []
        if len(formdata['email']) < 1 :
            errors.append("Email is required.")
        if len(formdata['password']) < 1 :
            errors.append("Password is required.")
        user = User.objects.filter(email=formdata['email']).first()
        if user:
            if not bcrypt.checkpw(formdata['password'].encode(), user.password.encode()) :
                errors.append("Email and password do not match.")
        result = {
            "errors": errors,
            "user": user,
        }
        return result

    def create_user(self, formdata):
        password = str(formdata['password'])
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = self.create (
            firstname = formdata['firstname'],
            lastname = formdata['lastname'],
            dob = formdata['dob'],
            email = formdata['email'],
            password = hashedpw,
        )
        return user

    def validate_edit(self, formdata):
        errors = []
        if len(formdata['firstname']) < 1 :
            errors.append("First name is required.")
        if len(formdata['lastname'])  < 1 :
            errors.append("Last name is required.")
        if len(formdata['email'])  < 1 :
            errors.append("Email is required.")
        if len(formdata['oldpassword']) > 0 :
            user = User.objects.filter(email=formdata['email']).first()
            if user:
                if not bcrypt.checkpw(formdata['oldpassword'].encode(), user.password.encode()) :
                    errors.append("Old password is incorrect.")
            if len(formdata['newpw'])  < 1 :
                errors.append("New password is required.")
            if formdata['newpw'] != formdata['newpwconfirm'] :
                errors.append("Confirm your new password.")
        return errors

    def edit_user(self, formdata):
        user = User.objects.get(id=formdata['id'])
        user.firstname = formdata['firstname']
        user.lastname = formdata['lastname']
        if formdata['newdob']:
            user.dob = formdata['newdob']
        user.email = formdata['email']
        if formdata['newpw']:
            password = str(formdata['password'])
            user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user.level = formdata['level']
        user.save()
        return user

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField(default=datetime.date.today)
    level = models.CharField(max_length=10, default="normal")
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
