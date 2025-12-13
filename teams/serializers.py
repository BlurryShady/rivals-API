from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Team, TeamMember, Vote, Comment
from heroes.serializers import HeroListSerializer

class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for team members (hero in a team slot)"""
    hero = HeroListSerializer(read_only=True)
    hero_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = TeamMember
        fields = ['id', 'hero', 'hero_id', 'position']

class UserSerializer(serializers.ModelSerializer):
    """Basic user info with avatar"""
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url']

    def get_avatar_url(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and profile.avatar:
            url = profile.avatar.url
            if url.startswith('http'):
                return url
            request = self.context.get('request')
            base = (
                request.build_absolute_uri('/')
                if request else 'http://127.0.0.1:8000/'
            )
            return f"{base.rstrip('/')}{url}"
        return None

class TeamListSerializer(serializers.ModelSerializer):
    """Team list with members for display"""
    user = UserSerializer(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    upvote_count = serializers.IntegerField(read_only=True)
    user_has_voted = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id',
            'slug',
            'name',
            'description',
            'user',
            'members',
            'member_count',
            'upvote_count',
            'user_has_voted',
            'composition_score',
            'views',
            'created_at',
        ]
    
    def get_member_count(self, obj):
        return obj.members.count()

    def get_user_has_voted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Vote.objects.filter(user=request.user, team=obj).exists()
        return False

class TeamDetailSerializer(serializers.ModelSerializer):
    """Full team with members and analysis"""
    user = UserSerializer(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    upvote_count = serializers.IntegerField(read_only=True)
    user_has_voted = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id',
            'slug',
            'name',
            'description',
            'user',
            'members',
            'analysis_data',
            'composition_score',
            'upvote_count',
            'user_has_voted',
            'views',
            'created_at',
            'updated_at',
        ]
    
    def get_user_has_voted(self, obj):
        """Check if current user has voted for this team"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Vote.objects.filter(user=request.user, team=obj).exists()
        return False

class TeamCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating teams"""
    members = TeamMemberSerializer(many=True)
    
    class Meta:
        model = Team
        fields = ['name', 'description', 'members']
    
    def validate_members(self, members):
        if len(members) != 6:
            raise serializers.ValidationError(
                "Team must include exactly 6 members."
            )

        positions = set()
        hero_ids = set()
        for member in members:
            position = member.get("position")
            hero_id = member.get("hero_id")

            if position in positions:
                raise serializers.ValidationError(
                    "Duplicate slot positions detected."
                )
            positions.add(position)

            if hero_id in hero_ids:
                raise serializers.ValidationError(
                    "A hero can only appear once per team."
                )
            hero_ids.add(hero_id)

        return members

    def _sync_members(self, team, members_data):
        TeamMember.objects.filter(team=team).delete()
        TeamMember.objects.bulk_create(
            [
                TeamMember(team=team, **member_data)
                for member_data in members_data
            ]
        )

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        with transaction.atomic():
            team = Team.objects.create(**validated_data)
            self._sync_members(team, members_data)
        return team

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        with transaction.atomic():
            instance.save()
            if members_data is not None:
                self._sync_members(instance, members_data)

        return instance


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
