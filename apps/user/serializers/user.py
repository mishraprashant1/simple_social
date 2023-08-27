from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from simple_social.models import User


class UserSignupSerializer(ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'country_code', 'phone_number', 'password',
                  'confirm_password']
        write_only_fields = ['password']

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match'})
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'password', 'last_login', 'is_superuser', 'is_staff', 'date_joined', 'is_active']
        read_only_fields = ['username', 'email']
