from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.status import HTTP_400_BAD_REQUEST

from main.services import MainService
from src import settings
from .models import Profile
from django.contrib.auth import get_user_model
from .choices import GenderChoice
from dj_rest_auth.serializers import PasswordChangeSerializer
from allauth.account.utils import setup_user_email

from .services import UserProfileService

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['gender', 'image', 'birthdate', 'bio', 'website']


class UserProfileSerializer(serializers.ModelSerializer):
    #    gender = serializers.ChoiceField(choices=GenderChoice.choices, source="profile.gender")
    profile = ProfileSerializer()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update(rep.pop("profile", {}))
        return rep

    class Meta:
        model = User
        fields = ['full_name', 'id', 'profile']


class TrueUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep.update(rep.pop("profile", {}))
        return rep

    class Meta:
        model = User
        fields = ['full_name', 'id', 'profile']


class ChangePasswordSerializer(PasswordChangeSerializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField(min_length=8)
    new_password2 = serializers.CharField(min_length=8)


class ChangeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image']

    def validate(self, attrs):
        limit = 4 * 1024 * 1024  # 4 mb
        if attrs.get('image').size > limit:
            raise serializers.ValidationError('File too large. Size should not exceed 4 MiB.')
        return attrs


class UserShortInfoSerializer(serializers.ModelSerializer):
    image = serializers.URLField(source='avatar_url')
    profile = serializers.URLField(source='get_absolute_url')

    class Meta:
        model = User
        fields = ('id', 'full_name', 'image', 'profile')


class GetUsersIdSerializer(serializers.Serializer):
    user_id = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        return attrs
