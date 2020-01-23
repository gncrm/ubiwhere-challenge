from api.models import Occurrence, User
import secrets
from django.utils import timezone
from math import sin, cos, sqrt, atan2, radians

class DbManager:

	'''The admin password is a code that admins must enter at account creation to be granted admin status'''
	admin_password = 'ABCDEFGH'

	'''
	This function checks if a category (argument) is one of the categories accepted by the API
	It converts the category it receives to uppercase for a better comparison
	'''
	def checkCategory(self, category):
		valid_categories = ['CONSTRUCTION', 'SPECIAL_EVENT', 'INCIDENT', 'WEATHER_CONDITION', 'ROAD_CONDITION']
		if category.upper() in valid_categories:
			return 1
		else:
			return 0

	'''
	This function checks if a location is valid, that is, if it is numeric and if -90 < latitude < 90 and -180 < longitude < 180
	'''
	def checkCoordinates(self, latitude, longitude):
		try:
			float(latitude)
			float(longitude)
		except:
			return 0
		if float(latitude) < -90.0 or float(latitude) > 90.0:
			return 0
		if float(longitude) < -180.0 or float(longitude) > 180.0:
			return 0
		return 1

	'''
	This function calculates and returns the distance between two locations passed as arguments
	'''
	def calculateDistance(self, latitude1, longitude1, latitude2, longitude2):
		latitude1 = radians(float(latitude1))
		latitude2 = radians(float(latitude2))
		longitude1 = radians(float(longitude1))
		longitude2 = radians(float(longitude2))

		aux = sin((latitude2 - latitude1) / 2)**2 + cos(latitude1) * cos(latitude2) * sin((longitude2 - longitude1) / 2)**2
		aux2 = 2 * atan2(sqrt(aux), sqrt(1 - aux))
		dist = 6373.0 * aux2
		return dist

	'''
	This function registers non admin users so they can use the API. It receives the desired username
	If the username already exists, it returns the proper error code
	If the username is available, it creates the database entry for the user, with a generated API token ,and returns the user information
	'''
	def registerUser(self, username):
		try:
			user = User.objects.get(pk = username)
			return 409
		except User.DoesNotExist:
			u = User(username = username, is_admin = False)
			u.api_token = secrets.token_hex(16)
			u.save()
			return u

	'''
	This function registers admins. It receives the desired username and the admin password to verify the admin status
	If the username already exists or the password is wrong it returns de appropriate error code
	If everything is correct, the database entry is created and the admin information is returned
	'''
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

	'''
	This function creates new occurrences. It receives the description, location, token of the creator and cateogry
	If the token does not exist, the coordinates are not valid or the cateogry is not valid, the appropriate error code is returned
	If everything is correct, the occurrence entry is created, with an unvalidated status and the current date and time as the creation date
	The information of the occurrence is then returned
	'''
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

	'''
	This function returns the list of all occurrences in the database, ordered from the most recent to the oldest
	'''
	def getOccurrenceList(self):
		return Occurrence.objects.all().order_by('-creation_date')

	'''
	This function returns information about the occurrence with the ID equal to the one received as argument
	If the occurrence does not exist the appropriate error code is returned
	'''
	def getOccurrenceDetails(self, pk):
		try:
			occ = Occurrence.objects.get(occ_id = pk)
			return occ
		except Occurrence.DoesNotExist:
			return 404

	'''
	This function updates the status of occurrences. It receives the ID and the token of the user trying to update it
	If the user is not an admin, the occurrence does not exist or its status is already solved, the appropriate error code is returned
	If everything is correct, the status is updated (unvalidated to validated or validated to solved) and the date of update is set to the current date and time
	The information of the occurrence is then returned
	'''
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

	'''
	This function returns the list of occurrences created by the user with the username received as argument, ordered from the most recent to the oldest
	'''
	def filterOccurrencesByUser(self, username):
		return Occurrence.objects.filter(user = username).order_by('-creation_date')

	'''
	This function returns the list of occurrences with the category received as argument, ordered from the most recent to the oldest
	If the category is invalid, the proper error code is returned
	'''
	def filterOccurrencesByCategory(self, categ):
		if self.checkCategory(categ):
			return Occurrence.objects.filter(category = categ.upper()).order_by('-creation_date')
		else:
			return 400

	'''
	This function returns the list of occurrences within radius of the location received as argument, ordered from the most recent to the oldest
	If the location is invalid or the radius is negative, the proper error code is returned
	'''
	def filterOccurrencesByLocation(self, latitude, longitude, radius):
		try:
			float(radius)
		except:
			return 400
		if self.checkCoordinates(latitude, longitude) and float(radius) >= 0:
			occ_list = Occurrence.objects.all().order_by('-creation_date')
			out = [occ for occ in occ_list if self.calculateDistance(latitude, longitude, occ.latitude, occ.longitude) <= float(radius)]
			return out
		else:
			return 400