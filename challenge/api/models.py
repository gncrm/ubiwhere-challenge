from django.db import models

# Create your models here.
class User(models.Model):
	username = models.CharField(primary_key = True, max_length = 20)
	api_token = models.CharField(max_length = 50)
	is_admin = models.BooleanField()

class Occurrence(models.Model):
	occ_id = models.AutoField(primary_key = True)
	description = models.CharField(max_length = 200)
	latitude = models.DecimalField(max_digits = 14, decimal_places = 10)
	longitude = models.DecimalField(max_digits = 14, decimal_places = 10)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	creation_date = models.DateTimeField()
	update_date = models.DateTimeField()
	status = models.CharField(max_length = 20)
	category = models.CharField(max_length = 20)
