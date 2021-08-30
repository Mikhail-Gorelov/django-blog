from rest_framework import serializers
from .models import Follower


# Create your serializers here.

class FollowerSerializer(serializers.ModelSerializer):
    to_user = serializers.IntegerField(min_value=1)

    class Meta:
        model = Follower
        fields = ('to_user', )

    def save(self):
        if self.validated_data["to_user"] is None:
            self.to_user = 296
        else:
            self.validated_data["to_user"] = None
        # 1) проверка на существование записи
        # 2) если записи нет
        # 3) создаём подписку
        # 4) иначе удаляем подписку
        print(self.validated_data)
        # return to_user_instance

    @property
    def data(self):
        return self.validated_data
