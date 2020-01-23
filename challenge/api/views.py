from api.models import Occurrence, User
from api.serializers import OccurrenceSerializer, UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from api.db_methods import DbManager
from django.http import HttpResponse
from django.template import loader
# Create your views here.

resp_codes = {200: status.HTTP_200_OK, 201: status.HTTP_201_CREATED, 400: status.HTTP_400_BAD_REQUEST, 
	401: status.HTTP_401_UNAUTHORIZED, 409: status.HTTP_409_CONFLICT, 404: status.HTTP_404_NOT_FOUND}

class UserRegistration(APIView):

	def post(self, request, format = None):
		db = DbManager()
		if 'username' in request.query_params:
			if 'admin_pw' in request.query_params:
				res = db.registerAdmin(request.query_params['username'], request.query_params['admin_pw'])
			else:
				res = db.registerUser(request.query_params['username'])
			if not isinstance(res, int):
				return Response(UserSerializer(res).data, status=resp_codes[201])
			else:
				return Response(status=resp_codes[res])
		else:
			return Response(status=resp_codes[400])

class OccurrenceList(APIView):

	def get(self, request, format = None):
		db = DbManager()
		if len(request.query_params) == 0:
			res = db.getOccurrenceList()
			return Response(OccurrenceSerializer(res, many = True).data, status=resp_codes[200])
		else:
			if 'username' in request.query_params:
				res = db.filterOccurrencesByUser(request.query_params['username'])
			elif 'category' in request.query_params:
				res = db.filterOccurrencesByCategory(request.query_params['category'])
			elif 'latitude' in request.query_params and 'longitude' in request.query_params and 'radius' in request.query_params:
				res = db.filterOccurrencesByLocation(request.query_params['latitude'], request.query_params['longitude'],
					request.query_params['radius'])
			else:
				return Response(status=resp_codes[400])
			if isinstance(res, int):
				return Response(status=resp_codes[res])
			else:
				return Response(OccurrenceSerializer(res, many = True).data, status=resp_codes[200])

	def post(self, request, format = None):
		db = DbManager()
		required_args = ['description', 'latitude', 'longitude', 'user_token', 'category']
		for req_arg in required_args:
			if req_arg not in request.query_params:
				return Response(status=resp_codes[400])
		res = db.addOccurrence(request.query_params['description'], request.query_params['latitude'], 
			request.query_params['longitude'], request.query_params['user_token'], request.query_params['category'])
		if isinstance(res, int):
			return Response(status=resp_codes[res])
		else:
			return Response(OccurrenceSerializer(res).data, status=resp_codes[201])

class OccurrenceDetail(APIView):

	def get(self, request, pk, format = None):
		db = DbManager()
		res = db.getOccurrenceDetails(pk)
		if isinstance(res, int):
			return Response(status=resp_codes[res])
		else:
			return Response(OccurrenceSerializer(res).data, status=resp_codes[200])

	def put(self, request, pk, format = None):
		db = DbManager()
		if 'user_token' in request.query_params:
			res = db.changeOccurrenceStatus(pk, request.query_params['user_token'])
			if isinstance(res, int):
				return Response(status=resp_codes[res])
			else:
				return Response(OccurrenceSerializer(res).data, status=resp_codes[200])
		else:
			return Response(status=resp_codes[401])

def api_help(request):
	template = loader.get_template('api/api_help.html')
	return HttpResponse(template.render())
