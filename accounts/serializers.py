from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserMiniSerializer(serializers.ModelSerializer):
    profileImg = serializers.ImageField(source="profile_img")
    userId = serializers.IntegerField(source="id")

    class Meta:
        model = User
        fields = (
            'userId', 'name', 'profileImg',
        )

class UserRankingSerializer(serializers.ModelSerializer):
    profileImg = serializers.ImageField(source="profile_img")
    userId = serializers.IntegerField(source="id")

    levelImg = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'userId', 'name', 'profileImg', 'exp', 'levelImg', 'level'
        )

    def get_levelImg(self,  obj):
        return ''

    def get_level(self,  obj):
        return ''

class UserSearchSerializer(serializers.ModelSerializer):
    profileImg = serializers.ImageField(source="profile_img")
    userId = serializers.IntegerField(source="id")
    userName = serializers.CharField(source="name")

    follow = serializers.SerializerMethodField()
    reviewCount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('userId', 'userName', 'profileImg', 'follow', 'reviewCount')
    
    def get_follow(self,  obj):
        return False

    def get_reviewCount(self,  obj):
        return obj.review_set.count()


class UserSerializer(serializers.ModelSerializer):
    profileImg = serializers.ImageField(source="profile_img")
    experience = serializers.IntegerField(source="exp")

    reviewCount = serializers.SerializerMethodField()
    followingCount = serializers.SerializerMethodField()
    followedCount = serializers.SerializerMethodField()
    follow = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    levelImg = serializers.SerializerMethodField()
    levelPercentage = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'name', 'profileImg', 'reviewCount', 'bio',
            'followingCount', 'followedCount', 'follow',
            'level', 'experience', 'levelImg', 'levelPercentage',
        )
    
    def get_reviewCount(self,  obj):
        return obj.review_set.count()
        
    def get_followingCount(self,  obj):
        return obj.followings.count()

    def get_followedCount(self,  obj):
        return obj.followers.count()

    def get_follow(self,  obj):
        return False

    def get_level(self,  obj):
        return 'Iron'

    def get_levelImg(self,  obj):
        return ''

    def get_levelPercentage(self,  obj):
        return 0


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
        user.save()

        return user
    
    def validate(self, data):
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user already exists")

        return data
