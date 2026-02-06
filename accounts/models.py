from django.db import models

# Create your models here.
# Customer Model
class Customer(models.Model):
    c_fullname = models.CharField(max_length=30)
    c_login_id = models.CharField(max_length=30, unique=True)
    c_password = models.CharField(max_length=100)
    c_contact = models.CharField(max_length=15)
    c_email = models.EmailField(unique=True)
    c_address = models.CharField(max_length=150)

    def __str__(self):
        return self.c_fullname

# Admin model
class AdminUser(models.Model):
    a_fullname = models.CharField(max_length=30)
    a_login_id = models.CharField(max_length=30, unique=True)
    a_password = models.CharField(max_length=100)
    a_contact = models.CharField(max_length=15)
    a_address = models.CharField(max_length=50)
    a_email = models.EmailField(unique=True)

    def __str__(self):
        return self.a_fullname


# Electrician Model
class Electrician(models.Model):
    e_fullname = models.CharField(max_length=30)
    e_login_id = models.CharField(max_length=30, unique=True)
    e_password = models.CharField(max_length=100)
    e_contact = models.CharField(max_length=15)
    e_qualification = models.CharField(max_length=50)
    e_address = models.CharField(max_length=50)
    e_email = models.EmailField(unique=True)
    status = models.CharField(max_length=20,default="Available")

    def __str__(self):
        return self.e_fullname
