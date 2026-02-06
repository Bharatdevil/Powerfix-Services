from django.db import models
from accounts.models import Electrician

class Service(models.Model):
    s_name = models.CharField(max_length=100)
    s_description = models.CharField(max_length=100)
    s_price = models.DecimalField(max_digits=8, decimal_places=2)

    #e_id = models.ForeignKey(Electrician,on_delete=models.CASCADE,db_column='e_id')

    def __str__(self):
        return self.s_name
