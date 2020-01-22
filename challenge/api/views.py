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