from api.models import Occurrence, User
import secrets

class DbManager:

	admin_password = 'ABCDEFGH'

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