from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import email_address_exists
from dj_rest_auth import serializers as auth_serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from main.services import CeleryService
from user_profile import choices

from .forms import PassResetForm
from .services import AuthAppService

User = get_user_model()

error_messages = {
    "not_verified": _("Email not verified"),
    "not_active": _("Your account is not active. Please contact Your administrator"),
    "wrong_credentials": _("Entered email or password is incorrect"),
}


class CaptchaSerializerMixin(serializers.Serializer):
    def validate(self, attrs):
        captcha_token = self.context["request"].POST.get("g-recaptcha-response")
        if not AuthAppService.validate_captcha(captcha_token, self.context["request"])[0]:
            raise serializers.ValidationError("Invalid captcha, try again")


class UserSignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=2, max_length=100, required=True)
    last_name = serializers.CharField(min_length=2, max_length=100, required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    birthday = serializers.DateField(required=True, source="profile.birthdate")
    gender = serializers.ChoiceField(
        required=True, choices=choices.GenderChoice.choices, source="profile.gender"
    )

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate_email(self, email) -> str:
        status, msg = AuthAppService.validate_email(email)
        if not status:
            raise serializers.ValidationError(msg)
        if email and email_address_exists(email):
            raise serializers.ValidationError(_("User is already registered with this e-mail address."))
        return email

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError({"password2": _("The two password fields didn't match.")})
        # if not data.get("birthdate"):
        #     raise serializers.ValidationError({"birthdate": "Birthdate is required"})
        # if not data.get("gender"):
        #     raise serializers.ValidationError({"gender": "Gender is required"})
        super(UserSignUpSerializer, self).validate(data)
        return data

    def save(self, **kwargs):
        profile = self.validated_data.pop("profile")
        request = self.context.get("request")
        self.validated_data["password"] = self.validated_data.pop("password1")
        del self.validated_data["password2"]
        if self.validated_data.get("captcha"):
            del self.validated_data["captcha"]
        user = User.objects.create_user(**self.validated_data, is_active=False)
        setup_user_email(request=request, user=user, addresses=[])
        for key, value in profile.items():
            setattr(user.profile, key, value)
        user.profile.save()
        CeleryService.send_email_confirm(user)
        return user

    @property
    def data(self):
        return self.validated_data


class LoginSerializer(auth_serializers.LoginSerializer):
    username = None
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = self._validate_email(email, password)
        if user:
            if not user.is_active:
                msg = {"email": error_messages["not_active"]}
                raise serializers.ValidationError(msg)
            email_address = user.emailaddress_set.get(email=user.email)
            if not email_address.verified:
                msg = {"email": error_messages["not_verified"]}
                raise serializers.ValidationError(msg)
        else:
            user = AuthAppService.get_user(email)
            if not user:
                msg = {"email": error_messages["wrong_credentials"]}
                raise serializers.ValidationError(msg)
            email_address = user.emailaddress_set.get(email=user.email)
            if not email_address.verified:
                msg = {"email": error_messages["not_verified"]}
                raise serializers.ValidationError(msg)
            if not user.is_active:
                msg = {"email": error_messages["not_active"]}
                raise serializers.ValidationError(msg)
            msg = {"email": error_messages["wrong_credentials"]}
            raise serializers.ValidationError(msg)
        attrs["user"] = user
        super(LoginSerializer, self).validate(attrs)
        return attrs


class UserSignUpWithCaptchaSerializer(UserSignUpSerializer):
    pass


class LoginWithCaptchaSerializer(LoginSerializer):
    pass


class PasswordResetSerializer(auth_serializers.PasswordResetSerializer):
    password_reset_form_class = PassResetForm


class PasswordResetConfirmSerializer(auth_serializers.PasswordResetConfirmSerializer):
    pass


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


class UserDataByCookieSerializer:
    pass
