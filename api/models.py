from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import now as now

# Create your models here.


# class Branch(models.Model):
#
#     type = models.CharField(max_length=256, blank=True, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
# class BranchWorker(models.Model):
#

class Branch(models.Model):
    address = models.CharField(max_length=256, blank=True, null=True, default="")

    location = models.CharField(max_length=256, blank=True, null=True, default="")
    working_hours = models.CharField(max_length=256, blank=True, null=True, default="")
    description = models.CharField(max_length=256, blank=True, null=True, default="")

class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)


class TeacherClass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, unique=False, default="")
    students = models.ManyToManyField(CustomUser, blank=True, related_name="classes")

class Lesson(models.Model):
    teacher_class =  models.ForeignKey(TeacherClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    sort_order = models.PositiveIntegerField(blank=True, unique=False, default=0)

# Create your models here.


class Item(models.Model):

    name = models.CharField(max_length=256, blank=True, null=True)
    inventory = models.PositiveIntegerField(default=0)
    price = models.FloatField(default=0)
    image = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, unique=False, default="")
    limit = models.PositiveIntegerField(default=0)

    log = models.TextField(blank=True, unique=False, default="")


class Order(models.Model):

    created = models.DateTimeField(
        editable=False, default=now, blank=True, null=True)
    items = models.TextField(blank=True, unique=False, default="")
    address = models.TextField(blank=True, unique=False, default="")
    total = models.PositiveIntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,  blank=True, null=True, related_name="orders", default=None)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  blank=True, null=True, related_name="orders", default=None)
    expected = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=256, blank=True, null=True, default="New")
    is_delivery = models.BooleanField(default=False)
