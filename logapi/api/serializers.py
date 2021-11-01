from rest_framework import serializers

from .models import UserDetails

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    
    class Meta:
        fields = ['username', 'email', 'password', 'password2']
        model = UserDetails

    def create(self, validate_data):
        username = validate_data.get('username')
        email = validate_data.get('email')
        password = validate_data.get('password')
        password2 = validate_data.get('password2')

        if password==password2:
            user = UserDetails(username=username, email=email)
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({
                'error': 'password does not match'
            })

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128)

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)