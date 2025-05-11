from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = str(user.id)
        # Get user groups (roles)
        token['groups'] = list(user.groups.values_list('name', flat=True))
        # Add role based on groups or superuser status
        if user.is_superuser:
            token['role'] = 'admin'
        elif user.groups.filter(name='admin').exists():
            token['role'] = 'admin'
        else:
            token['role'] = 'user'

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'phone', 'gender', 'image', 'status')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            gender=validated_data.get('gender'),
            image=validated_data.get('image', ''),
            status=validated_data.get('status', ''),
        )
        user.set_password(validated_data['password'])
        user.save()

        # Gán người dùng vào nhóm 'user' mặc định
        user_group, _ = Group.objects.get_or_create(name='user')
        user.groups.add(user_group)

        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'gender', 'image', 'status', 'role')

    def get_role(self, obj):
        if obj.is_superuser:
            return 'admin'
        elif obj.groups.filter(name='admin').exists():
            return 'admin'
        return 'user'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class SocialLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    provider = serializers.CharField(required=True)