from api.models import Occurrence, User
import secrets
from django.utils import timezone

class DbManager:

	admin_password = 'ABCDEFGH'

	def checkCategory(self, category):
		valid_categories = ['CONSTRUCTION', 'SPECIAL_EVENT', 'INCIDENT', 'WEATHER_CONDITION', 'ROAD_CONDITION']
		if category.upper() in valid_categories:
			return 1
		else:
			return 0

	def checkCoordinates(self, latitude, longitude):
		if float(latitude) < -90.0 or float(latitude) > 90.0:
			return 0
		if float(longitude) < -180.0 or float(longitude) > 180.0:
			return 0
		return 1

	def registerUser(self, username):
		try:
			user = User.objects.get(pk = username)
			return -1
		except User.DoesNotExist:
			u = User(username = username, is_admin = False)
			u.api_token = secrets.token_hex(16)
			u.save()
			return u

	def registerAdmin(self, username, pw):
		try:
			user = User.objects.get(pk = username)
			return -1
		except User.DoesNotExist:
			if pw == self.admin_password:
				u = User(username = username, is_admin = True)
				u.api_token = secrets.token_hex(16)
				u.save()
				return u
			else:
				return -2

	#occ_id, description, latitude, longitude, user, creation_date, update_date, status, category

	def addOccurrence(self, description, latitude, longitude, user_token, category):
		try:
			user = User.objects.get(api_token = user_token)
			if self.checkCoordinates(latitude, longitude) and self.checkCategory(category):
				occ = Occurrence(description = description, latitude = latitude, longitude = longitude,
					user = user, category = category.upper())
				occ.creation_date = timezone.now()
				occ.status = 'unvalidated'
				occ.save()
				return occ
			else:
				return None
		except User.DoesNotExist:
			return -1