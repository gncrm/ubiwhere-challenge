from django.test import TestCase

from .models import User, Occurrence
from .db_methods import DbManager

# Create your tests here.
'''
This class contains tests for the functions from DbManager that provide checks on the validity of the data
'''
class CheckFunctionsTests(TestCase):

	def test_category_check_with_correct_category(self):
		db = DbManager()
		self.assertEqual(db.checkCategory('construction'), 1)
		self.assertEqual(db.checkCategory('Special_Event'), 1)
		self.assertEqual(db.checkCategory('INCIdent'), 1)
		self.assertEqual(db.checkCategory('WEATHER_CONDITION'), 1)
		self.assertEqual(db.checkCategory('road_condition'), 1)

	def test_category_check_with_incorrect_category(self):
		db = DbManager()
		self.assertEqual(db.checkCategory('random_category'), 0)
		self.assertEqual(db.checkCategory('1234'), 0)

	def test_coordinate_check_with_correct_coordinates(self):
		db = DbManager()
		self.assertEqual(db.checkCoordinates('80.0', '50.0'), 1)
		self.assertEqual(db.checkCoordinates('-80.0', '50.0'), 1)
		self.assertEqual(db.checkCoordinates('80.0', '-50.0'), 1)
		self.assertEqual(db.checkCoordinates('-80.0', '-50.0'), 1)

	def test_coordinate_check_with_incorrect_coordinates(self):
		db = DbManager()
		self.assertEqual(db.checkCoordinates('200.0', '50.0'), 0)
		self.assertEqual(db.checkCoordinates('-1080.0', '50.0'), 0)
		self.assertEqual(db.checkCoordinates('80.0', '-500.0'), 0)
		self.assertEqual(db.checkCoordinates('-80.0', '500.0'), 0)
		self.assertEqual(db.checkCoordinates('-800.0', '500.0'), 0)
		self.assertEqual(db.checkCoordinates('text', '500.0'), 0)
		self.assertEqual(db.checkCoordinates('200.0', 'text'), 0)
		self.assertEqual(db.checkCoordinates('text', 'text'), 0)

'''
This class contains tests for the functions of DbManager that register users and admins
'''
class UserRegistrationTests(TestCase):

	def test_user_registration_already_exists(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		res = db.registerUser('user1')
		self.assertEqual(res, 409)

	def test_user_registration_sucess(self):
		db = DbManager()
		res = db.registerUser('user2')
		self.assertEqual(True, isinstance(res, User))

	def test_admin_registration_already_exists(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		res = db.registerAdmin('user1', 'ABCDEFGH')
		self.assertEqual(res, 409)

	def test_admin_registration_wrong_password(self):
		db = DbManager()
		res = db.registerAdmin('user2', 'wrong_password')
		self.assertEqual(res, 400)

	def test_admin_registration_sucess(self):
		db = DbManager()
		res = db.registerAdmin('user2', 'ABCDEFGH')
		self.assertEqual(True, isinstance(res, User))

'''
This class contains tests for the functions of DbManager related to creating, reading and updating occurrences
'''
class OccurrenceFunctionsTests(TestCase):

	def test_add_occurrence_wrong_api_token(self):
		db = DbManager()
		res = db.addOccurrence('description', '0.0', '0.0', 'non_existent_user_token', 'weather_condition')
		self.assertEqual(res, 401)

	def test_add_occurrence_wrong_coordinates(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		res = db.addOccurrence('description', '200.0', '-400.0', u1.api_token, 'weather_condition')
		self.assertEqual(res, 400)

	def test_add_occurrence_wrong_category(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		res = db.addOccurrence('description', '0.0', '0.0', u1.api_token, 'weather')
		self.assertEqual(res, 400)

	def test_add_occurrence_sucess(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		res = db.addOccurrence('description', '0.0', '0.0', u1.api_token, 'weather_condition')
		self.assertEqual(True, isinstance(res, Occurrence))

	def test_get_non_existant_occurrence_details(self):
		db = DbManager()
		res = db.getOccurrenceDetails(20)
		self.assertEqual(res, 404)

	def test_get_occurrence_details_sucess(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		occ = db.addOccurrence('description', '0.0', '0.0', u1.api_token, 'weather_condition')
		res = db.getOccurrenceDetails(int(occ.occ_id))
		self.assertEqual(True, isinstance(res, Occurrence))

	def test_change_occurrence_status_wrong_api_token(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		occ = db.addOccurrence('description', '0.0', '0.0', u1.api_token, 'weather_condition')
		res = db.changeOccurrenceStatus(int(occ.occ_id), 'wrong_api_token')
		self.assertEqual(res, 401)

	def test_change_occurrence_status_user_not_admin(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = False)
		u1.save()
		occ = db.addOccurrence('description', '0.0', '0.0', u1.api_token, 'weather_condition')
		res = db.changeOccurrenceStatus(int(occ.occ_id), u1.api_token)
		self.assertEqual(res, 401)

	def test_change_occurrence_status_non_existant_occurrence(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = True)
		u1.save()
		res = db.changeOccurrenceStatus(20, u1.api_token)
		self.assertEqual(res, 404)

	def test_change_occurrence_status_already_solved(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = True)
		u1.save()
		occ = db.addOccurrence('description', '0.0', '0.0', u1.api_token, 'weather_condition')
		occ.status = 'solved'
		occ.save()
		res = db.changeOccurrenceStatus(int(occ.occ_id), u1.api_token)
		self.assertEqual(res, 400)

	def test_change_occurrence_status_sucess(self):
		db = DbManager()
		u1 = User(username = 'user1', is_admin = True)
		u1.save()
		occ = db.addOccurrence('description', '0.0', '0.0', u1.api_token, 'weather_condition')
		res = db.changeOccurrenceStatus(int(occ.occ_id), u1.api_token)
		self.assertEqual(True, isinstance(res, Occurrence))
		res = db.changeOccurrenceStatus(int(occ.occ_id), u1.api_token)
		self.assertEqual(True, isinstance(res, Occurrence))

'''
This class contains tests for the functions of DbManager that filter the existing occurrences based on a parameter
'''
class OccurrenceFiltersTests(TestCase):

	def test_filter_occurrences_by_category_invalid_category(self):
		db = DbManager()
		res = db.filterOccurrencesByCategory('invalid_category')
		self.assertEqual(res, 400)

	def test_filter_occurrences_by_location_invalid_radius(self):
		db = DbManager()
		res = db.filterOccurrencesByLocation('0.0', '0.0', '-500')
		self.assertEqual(res, 400)
		res = db.filterOccurrencesByLocation('0.0', '0.0', 'radius')
		self.assertEqual(res, 400)

	def test_filter_occurrences_by_location_invalid_coordinates(self):
		db = DbManager()
		res = db.filterOccurrencesByLocation('-1000.0', '500.0', '500')
		self.assertEqual(res, 400)
		res = db.filterOccurrencesByLocation('latitude', 'longitude', '500')
		self.assertEqual(res, 400)

	def test_filter_occurrences_by_location_sucess(self):
		db = DbManager()
		res = db.filterOccurrencesByLocation('0.0', '0.0', '500')
		self.assertEqual(True, isinstance(res, list))