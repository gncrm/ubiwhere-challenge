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
			return 409
		except User.DoesNotExist:
			u = User(username = username, is_admin = False)
			u.api_token = secrets.token_hex(16)
			u.save()
			return u

	def registerAdmin(self, username, pw):
		try:
			user = User.objects.get(pk = username)
			return 409
		except User.DoesNotExist:
			if pw == self.admin_password:
				u = User(username = username, is_admin = True)
				u.api_token = secrets.token_hex(16)
				u.save()
				return u
			else:
				return 400

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
				return 400
		except User.DoesNotExist:
			return 401

	def getOccurrenceList(self):
		return Occurrence.objects.all().order_by('-creation_date')

	def getOccurrenceDetails(self, pk):
		try:
			occ = Occurrence.objects.get(occ_id = pk)
			return occ
		except Occurrence.DoesNotExist:
			return 404

	def changeOccurrenceStatus(self, pk, user_token):
		try:
			user = User.objects.get(api_token = user_token)
			if user.is_admin == False:
				return 401
			try:
				occ = Occurrence.objects.get(occ_id = pk)
				if occ.status == 'unvalidated':
					occ.status = 'validated'
					occ.update_date = timezone.now()
					occ.save()
				elif occ.status == 'validated':
					occ.status = 'solved'
					occ.update_date = timezone.now()
					occ.save()
				else:
					return 400
				return occ
			except Occurrence.DoesNotExist:
				return 404
		except User.DoesNotExist:
			return 401

	def filterOccurrencesByUser(self, username):
		return Occurrence.objects.filter(user = username).order_by('-creation_date')

	def filterOccurrencesByCategory(self, categ):
		if self.checkCategory(categ):
			return Occurrence.objects.filter(category = categ.upper()).order_by('-creation_date')
		else:
			return 400

	def filterOccurrencesByLocation(self, latitude, longitude, radius):
		if self.checkCoordinates(latitude, longitude) and radius >= 0:
			pass
		else:
			return 400