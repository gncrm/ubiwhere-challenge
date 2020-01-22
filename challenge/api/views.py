from api.models import Occurrence, User
from api.serializers import OccurrenceSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from api.db_methods import DbManager 
# Create your views here.

#Admin do sistema: da5fb0fa317f84a06990ccc5e71864f7

class UserRegistration(APIView):

	def post(self, request, format = None):
		db = DbManager()
		if 'username' in request.query_params:
			if 'admin_pw' in request.query_params:
				res = db.registerAdmin(request.query_params['username'], request.query_params['admin_pw'])
			else:
				res = db.registerUser(request.query_params['username'])
			if res != -1 and res != -2:
				return Response(UserSerializer(res).data)
			else:
				return JsonResponse({}, status = 200)
		else:
			return JsonResponse({}, status = 200)

class OccurrenceList(APIView):

	#[occ_id], description, latitude, longitude, user, [creation_date], [update_date], [status], category

	def get(self, request, format = None):
		db = DbManager()
		res = db.getOccurrenceList()
		return Response(OccurrenceSerializer(res, many = True).data)

	def post(self, request, format = None):
		db = DbManager()
		required_args = ['description', 'latitude', 'longitude', 'user_token', 'category']
		for req_arg in required_args:
			if req_arg not in request.query_params:
				return JsonResponse({}, status = 200)
		res = db.addOccurrence(request.query_params['description'], request.query_params['latitude'], 
			request.query_params['longitude'], request.query_params['user_token'], request.query_params['category'])
		if res == None:
			return JsonResponse({}, status = 200)
		elif res == -1:
			return JsonResponse({}, status = 200)
		else:
			return Response(OccurrenceSerializer(res).data)

class OccurrenceDetail(APIView):

	def get(self, request, pk, format = None):
		db = DbManager()
		res = db.getOccurrenceDetails(pk)
		if res == -1:
			return JsonResponse({}, status = 200)
		else:
			return Response(OccurrenceSerializer(res).data)

	def post(self, request, pk, format = None):
		db = DbManager()
		if 'user_token' in request.query_params:
			res = db.changeOccurrenceStatus(pk, request.query_params['user_token'])
			if res == None or res == -1:
				return JsonResponse({}, status = 200)
			else:
				return Response(OccurrenceSerializer(res).data)
		else:
			return JsonResponse({}, status = 200)