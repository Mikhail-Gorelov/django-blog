from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=False)
    name = serializers.CharField(min_length=2, required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'content', 'file')

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.is_authenticated:
            if not attrs.get('email') and not attrs.get('name') and not attrs.get('content'):
                raise serializers.ValidationError(
                    {
                        "name": "field is required",
                        "email": "field is required",
                        "content": "field is required",
                    }
                )
            if not attrs.get('email') and not attrs.get('name'):
                raise serializers.ValidationError({"name": "field is required", "email": "field is required"})
            if not attrs.get('email') and not attrs.get('content'):
                raise serializers.ValidationError(
                    {"email": "field is required", "content": "field is required"}
                )
            if not attrs.get('name') and not attrs.get('content'):
                raise serializers.ValidationError(
                    {"name": "field is required", "content": "field is required"}
                )
            if not attrs.get('name'):
                raise serializers.ValidationError({"name": "field is required"})
            if not attrs.get('email'):
                raise serializers.ValidationError({"email": "field is required"})

        if not attrs.get('content'):
            raise serializers.ValidationError({"content": "field is required"})

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['name'] = user.full_name()
            validated_data['email'] = user.email
        return super().create(validated_data)
