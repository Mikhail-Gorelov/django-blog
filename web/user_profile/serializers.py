from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model
from .choices import GenderChoice
from dj_rest_auth.serializers import PasswordChangeSerializer

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
