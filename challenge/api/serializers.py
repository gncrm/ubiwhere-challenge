from rest_framework import serializers
from api.models import Occurrence, User


class OccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        fields = ['occ_id', 'description', 'latitude', 'longitude', 'user', 'creation_date', 'update_date', 'status', 'category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'api_token', 'is_admin']