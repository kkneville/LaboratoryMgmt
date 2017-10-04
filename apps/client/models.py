from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import random, re
import bcrypt
import datetime
from ..lab.models import Hospital, ReferenceLab

# -------------------------
# A practice is legal billing entity that has one or more providers associated with it. Generally, in a group practice, all providers will bill under a shared tax id. In the case of a large network of group providers, this may be an even more generalised tax id. When the practice is private and consists of only a single provider, they may bill under that providers NPI. Typically, reps interact with provider groups at the office level.

class PracticeManager(models.Manager):
    def create_office(self, formdata):
        rep = Rep.objects.get(id=formdata['repid'])
        practice = self.create(
            name = formdata['name'],
            practice_email = formdata['practice_email'],
            practice_phone = formdata['practice_phone'],
            address = formdata['address'],
            city = formdata['city'],
            state = formdata['state'],
            zipcode = formdata['zipcode'],
            taxid = formdata['taxid'],
            comments = formdata['comments'],
            rep = rep,
        )
        return practice

class Practice(models.Model):
    name = models.CharField(max_length=200)
    practice_email = models.CharField(max_length=200)
    practice_phone = models.IntegerField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField(max_length=5)
    taxid = models.InteferField(max_length=20)
    rep = models.ForeignKeyField(Rep, related_name="practices")
    comments = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PracticeManager()

# ----------------------------
# Providers are any individual able to order labwork. Generally this will be an MD, DO, PA, NP, and sometimes a DC. Supervisory relationships can be noted in the comments if applicable.

class ProviderManager(models.Model):
    def create_provider(self, formdata):
        password = str(formdata['password'])
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        practice = Practice.objects.get(id=formdata['practiceid'])
        provider = self.create(
            firstname = formdata['firstname'],
            lastname = formdata['lastname'],
            designation = formdata['designation'],
            email = formdata['email'],
            private_phone = formdata['private_phone'],
            npi = formdata['npi'],
            password = hashedpw,
            practice = practice,
            comments = formdata['comments'],
        )
        return provider

class Provider(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    designation = models.CharField(max_length=4)
    email = models.CharField(max_length=200)
    private_phone = models.IntegerField()
    npi = models.IntegerField(max_length=20)
    password = models.CharField(max_length=100)
    practice = models.ForeignKeyField(Rep, related_name="physicians")
    comments = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProviderManager()

# ---------------------------
# Contacts are any person with direct access to provider and patient information, generally employees at the provider practice. These many be office managers, clinical, or administrative staff. Sometimes there will be a specific contact for each provider in the group, other times multiple contacts or a single conduit exist, so this model has been created to be versatile and accommodate different communication structures.

class ContactManager(models.Manager):
    def create_contact(self, formdata):
        password = str(formdata['password'])
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        practice = Practice.objects.get(id=formdata['practiceid'])
        provider = Provider.objects.get(id=formdata['providerid'])
        contact = self.create(
            firstname = formdata['firstname'],
            lastname = formdata['lastname'],
            email = formdata['email'],
            private_phone = formdata['private_phone'],
            password = hashedpw,
            practice = practice,
            providers = provider,
            comments = formdata['comments'],
        )
        return contact

class Contact(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    private_phone = models.IntegerField()
    practice = models.ForeignKeyField(Practice, related_name"employees")
    providers = models.ForeignKeyField(Provider, related_name="contacts")
    comments = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ContactManager()

# --------------------
# Repgroups consist of reps who handle their own accounts, and as a group they will broker relationships with facilities like independent labs and hospitals for the purposes of reference work and billing.

class RepGroupManager(models.Manager):
    def create_repgroup(self, formdata):
        repgroup = self.create (
            name = formdata['name'],
            primary_contact = formdata['primary_contact'],
            private_phone = formdata['private_phone'],
            email = formdata['email'],
            contracts = formdata['contract'],
            comments = formdata['comments'],
        )

class RepGroup(models.Model):
    name = models.CharField(max_length=100)
    primary_contact = models.CharField(max_length=100)
    private_phone = models.IntegerField()
    email = models.CharField(max_length=200)
    contracts = models.CharField(max_length=100)
    hospital = models.ForeignKeyField(Hospital, related_name="repgroup")
    referencelab = models.ForeignKeyField(ReferenceLab, related_name="repgroup")
    comments = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RepGroupManager()

# ----------------
# Reps generally work in groups but have their own accounts to handle. Depending on how hands-on they are, they may or may not want to be the main conduit through which the facility contacts the provider practice. They need access to some but not all patient and sample data, in order to assess the performance of their accounts, and for the purpose of identifying and resolving conflicts over specific samples.

class RepManager(models.Manager):
    def create_rep(self, formdata):
        password = str(formdata['password'])
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        repgroup = RepGroup.objects.get(id = formdata['repgroup.id'])
        rep = self.create (
            firstname = formdata['firstname'],
            lastname = formdata['lastname'],
            email = formdata['email'],
            private_phone = formdata['private_phone'],
            password = hashedpw,
            repgroup = repgroup,
            comments = formdata['comments'],
        )
        return rep

class Rep(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    private_phone = models.IntegerField()
    password = models.CharField(max_length=100)
    repgroup = models.ForeignKeyField(RepGroup, related_name="reps")
    comments = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RepManager()
