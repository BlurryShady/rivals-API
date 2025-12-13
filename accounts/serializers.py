from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from teams.models import Team, Vote
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    team_count = serializers.SerializerMethodField()
    upvote_count = serializers.SerializerMethodField()
    upvotes_received = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar_url', 'team_count', 'upvote_count', 'upvotes_received', 'bio')

    def get_avatar_url(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and profile.avatar:
            url = profile.avatar.url
            if url.startswith('http'):
                return url
            request = self.context.get('request')
            base = request.build_absolute_uri('/') if request else 'http://127.0.0.1:8000/'
            return base.rstrip('/') + url
        return None

    def get_team_count(self, obj):
        try:
            return Team.objects.filter(user=obj).count()
        except Exception:
            return 0

    def get_upvote_count(self, obj):
        try:
            return Vote.objects.filter(user=obj).count()
        except Exception:
            return 0
    
    def get_upvotes_received(self, obj):
        try:
            return Vote.objects.filter(team__user=obj).count()
        except Exception:
            return 0
    
    def get_bio(self, obj):
        profile = getattr(obj, 'profile', None)
        return profile.bio if profile else ''

class ProfileUpdateSerializer(serializers.ModelSerializer):
    clear = serializers.BooleanField(write_only=True, required=False, default=False)
    avatar = serializers.ImageField(required=False, allow_null=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'clear')

    def update(self, instance, validated_data):
        clear = validated_data.pop('clear', False)
        if clear:
            instance.avatar = None
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
