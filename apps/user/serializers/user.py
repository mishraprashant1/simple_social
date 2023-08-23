from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from simple_social.models import User


class UserSerializer(ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'country_code', 'phone_number', 'password',
                  'confirm_password']
        write_only_fields = ['password']

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            country_code=self.validated_data['country_code'],
            phone_number=self.validated_data['phone_number'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Password fields didn\'t match'})
        return attrs
