from rest_framework import serializers
from .models import Hero

class HeroListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for hero lists (no relationships)"""
    synergies = serializers.SerializerMethodField()
    counters = serializers.SerializerMethodField()
    
    class Meta:
        model = Hero
        fields = [
            'id',
            'name',
            'role',
            'image',
            'banner',
            'description',
            'difficulty',
            'playstyle_tags',
            'synergies',
            'counters',
        ]
    
    def get_synergies(self, obj):
        """Return synergy hero names only"""
        return [hero.name for hero in obj.synergies.all()]
    
    def get_counters(self, obj):
        """Return counter hero names only"""
        return [hero.name for hero in obj.counters.all()]

class HeroDetailSerializer(serializers.ModelSerializer):
    """Full serializer with synergies/counters"""
    synergies = serializers.SerializerMethodField()
    counters = serializers.SerializerMethodField()
    countered_by = serializers.SerializerMethodField()
    
    class Meta:
        model = Hero
        fields = [
            'id',
            'name',
            'role',
            'image',
            'banner',
            'description',
            'difficulty',
            'playstyle_tags',
            'synergies',
            'counters',
            'countered_by',
            'video_url',
            'tips',
            'created_at',
        ]
    
    def get_synergies(self, obj):
        """Return synergy heroes (basic info only)"""
        return [
            {
                'id': hero.id,
                'name': hero.name,
                'role': hero.role,
                'image': hero.image.url if hero.image else None,
            }
            for hero in obj.synergies.all()
        ]
    
    def get_counters(self, obj):
        """Return heroes this hero counters (Good Against)"""
        return [
            {
                'id': hero.id,
                'name': hero.name,
                'role': hero.role,
                'image': hero.image.url if hero.image else None,
            }
            for hero in obj.counters.all()
        ]
    
    def get_countered_by(self, obj):
        """Return heroes that counter this hero (Bad Against)"""
        countered_by_heroes = Hero.objects.filter(counters=obj)
        return [
            {
                'id': hero.id,
                'name': hero.name,
                'role': hero.role,
                'image': hero.image.url if hero.image else None,
            }
            for hero in countered_by_heroes
        ]