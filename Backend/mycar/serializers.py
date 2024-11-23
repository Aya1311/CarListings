from django.contrib.auth import get_user_model
from rest_framework import serializers
from mycar.models import CarAvito, CarMoteur, Admin, Client

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()  

    class Meta:
        model = Client
        fields = ['user', 'age', 'budget_min', 'budget_max', 'boite_preferee', 'carburant_prefere']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ['user', 'role']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        admin = Admin.objects.create(user=user, **validated_data)
        return admin
class CarAvitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarAvito
        fields = '__all__'

class CarMoteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMoteur
        fields = '__all__'
