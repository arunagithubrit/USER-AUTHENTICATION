from rest_framework import serializers
from user.models import Registration

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)
    class Meta:
        model=Registration
        fields=["id","username","email","password","is_verified"]


    # def create(self, validated_data):
    #     return Registration.objects.create_user(**validated_data)
        

