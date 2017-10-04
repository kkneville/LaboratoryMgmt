from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import random, re
import bcrypt
import datetime
from ..client.models import Provider

class PatientManager(models.Manager):
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
        patient = Patient.objects.filter(email=formdata['email']).first()
        if patient:
            if not bcrypt.checkpw(formdata['password'].encode(), patient.password.encode()) :
                errors.append("Email and password do not match.")
        result = {
            "errors": errors,
            "patient": patient,
        }
        return result

    def create_patient(self, formdata):
        password = str(formdata['password'])
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        patient = self.create (
            firstname = formdata['firstname'],
            lastname = formdata['lastname'],
            dob = formdata['dob'],
            email = formdata['email'],
            password = hashedpw,
        )
        return patient

    def validate_edit(self, formdata):
        errors = []
        if len(formdata['firstname']) < 1 :
            errors.append("First name is required.")
        if len(formdata['lastname'])  < 1 :
            errors.append("Last name is required.")
        if len(formdata['email'])  < 1 :
            errors.append("Email is required.")
        if len(formdata['oldpassword']) > 0 :
            patient = Patient.objects.filter(email=formdata['email']).first()
            if patient:
                if not bcrypt.checkpw(formdata['oldpassword'].encode(), patient.password.encode()) :
                    errors.append("Old password is incorrect.")
            if len(formdata['newpw'])  < 1 :
                errors.append("New password is required.")
            if formdata['newpw'] != formdata['newpwconfirm'] :
                errors.append("Confirm your new password.")
        return errors

    def edit_patient(self, formdata):
        patient = Patient.objects.get(id=formdata['id'])
        patient.firstname = formdata['firstname']
        patient.lastname = formdata['lastname']
        if formdata['newdob']:
            patient.dob = formdata['newdob']
        patient.email = formdata['email']
        if formdata['newpw']:
            password = str(formdata['password'])
            patient.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        patient.level = formdata['level']
        patient.save()
        return patient


class Patient(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.IntegerField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField(max_length=5)
    dob = models.DateField(default=datetime.date.today)
    provider = models.ForeignKeyField(Provider, related_name="patient")
    carrier = models.CharField(max_length=20)
    network = models.CharField(max_length=100)
    insid = models.CharField(max_length=20)
    insgrp = models.CharField(max_length=20)
    insphone = models.IntegerField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PatientManager()
