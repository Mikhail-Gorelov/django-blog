from rest_framework import serializers
from .models import Follower


# Create your serializers here.

class FollowerSerializer(serializers.ModelSerializer):
    to_user = serializers.IntegerField(min_value=1)

    class Meta:
        model = Follower
        fields = ('to_user', )

    def create(self, validated_data, to_user):
        instance = Follower(**validated_data)
        instance.save()
        return instance

    def save(self, **kwargs):
        print(self.validated_data)
        to_user_instance = Follower.objects.create(**self.validated_data)
        request = self.context.get('request')
        if request == 'delete':
            del self.validated_data['another thing']
            del to_user_instance
        return to_user_instance

    @property
    def data(self):
        return self.validated_data
