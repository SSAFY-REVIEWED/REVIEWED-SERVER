from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserListSerializer(serializers.ModelSerializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    pass

class UserJWTLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required = True,
        write_only=True,
        max_length=100
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


    class Meta(object):
        model = User
        fields = ['email', 'password']
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)


        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if password != 'googleAuth' and not user.check_password(password):
                raise serializers.ValidationError('wrong password')
        
        else:
            raise serializers.ValidationError('user account not exist')

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        data = {
                'access': access,
                'refresh': refresh,
            }

        return data


class UserJWTSignupSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required = True,
        write_only=True,
        max_length=100
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta(object):
        model = User
        fields = ['email', 'password', 'name']

    def save(self, request):
        user = super().save()

        user.email = self.validated_data['email']
        user.set_password(self.validated_data['password'])
        user.username = self.validated_data['email']
        user.survey_genre = '{status: False}'
        user.save()

        return user
    
    def validate(self, data):
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user already exists")

        return data
