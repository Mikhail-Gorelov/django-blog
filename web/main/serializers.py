import pytz
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from user_profile.serializers import UserShortInfoSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "email")


class SetTimeZoneSerializer(serializers.Serializer):
    timezone = serializers.ChoiceField(choices=pytz.common_timezones)


class ValidateJWTSerializer(serializers.Serializer):
    auth = serializers.CharField()

    def validate_auth(self, jwt: str):
        try:
            access_token = AccessToken(jwt)
            print(access_token["user_id"])
            self.user = User.objects.get(pk=access_token["user_id"])
        except (TokenError, User.DoesNotExist) as e:
            raise serializers.ValidationError(e)
        return jwt

    @property
    def response_data(self) -> dict:
        print(self.context)
        return UserShortInfoSerializer(self.user, context=self.context).data


class ReturnUsersSerializer(serializers.Serializer):
    @property
    def response_data(self) -> dict:
        print(self.context)
        return UserShortInfoSerializer(self.user, context=self.context).data
