from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import random, re
import bcrypt
import datetime
from ..patient.models import Patient
from ..client.models import Provider


class SampleManager(models.Manager):
    def create_sample(self, formdata):
        patient = Patient.objects.get(id=formdata['patientid'])
        sample = self.create(
            patient = patient,
            sample_type = formdata['sample_type'],
            status = formdata['status'],
        )
        return sample

class Sample(models.Model):
    patient = models.ForeignKeyField(Patient, related_name="sample_from")
    ordering_provider = models.ForeignKeyField(Provider, related_name="ordered_by")
    sample_type = models.CharField(max_length=20)
    ordered_tests = models.ForeignKeyField(Order, related_name="sample_for")
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SampleManager()


class OrderManager(models.Manager):
    def create_sample(self, formdata):
        sample = Sample.objects.get(id=formdata['sampleid'])
        order = self.create(
            sample = sample,
            content = formdata['content'],
        )
        return sample

class Order(models.Model):
    sample = models.ForeignKeyField(Sample, related_name="tests_ordered")
    content = models.CharField(max_length="500")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrderManager()


class ReferenceLabManager(models.Manager):
    def create_referencelab(self, formdata):
        referencelab = self.create(
            name = formdata['name'],
            address = formdata['address'],
            city = formdata['city'],
            state = formdata['state'],
            zipcode = formdata['zipcode'],
            taxid = formdata['taxid'],
            office_phone = formdata['office_phone'],
        )

class ReferenceLab(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField(max_length=5)
    taxid = models.InteferField(max_length=20)
    office_phone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object = ReferenceLabManager()