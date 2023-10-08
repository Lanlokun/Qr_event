# event_app/serializers.py

from rest_framework import serializers
from .models import Event, Participant, ParticipantType, AccessCoupon, CouponType
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ParticipantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantType
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    # participant_type = ParticipantTypeSerializer()

    class Meta:
        model = Participant
        fields = '__all__'


class AccessCouponSerializer(serializers.ModelSerializer):
    # participant = ParticipantSerializer()


    class Meta:
        model = AccessCoupon
        fields = '__all__'

class CouponTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponType
        fields = '__all__'
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            password=validated_data['password']
        )
        return user