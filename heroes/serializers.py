from rest_framework import serializers
from .models import Hero

class HeroListSerializer(serializers.ModelSerializer):
    synergies = serializers.SerializerMethodField()
    counters = serializers.SerializerMethodField()

    image_url = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()

    class Meta:
        model = Hero
        fields = [
            "id",
            "name",
            "role",
            "image_url",
            "banner_url",
            "description",
            "difficulty",
            "playstyle_tags",
            "synergies",
            "counters",
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_banner_url(self, obj):
        return obj.banner.url if obj.banner else None

    def get_synergies(self, obj):
        return [hero.name for hero in obj.synergies.all()]

    def get_counters(self, obj):
        return [hero.name for hero in obj.counters.all()]


class HeroDetailSerializer(serializers.ModelSerializer):
    synergies = serializers.SerializerMethodField()
    counters = serializers.SerializerMethodField()
    countered_by = serializers.SerializerMethodField()

    image_url = serializers.SerializerMethodField()
    banner_url = serializers.SerializerMethodField()

    class Meta:
        model = Hero
        fields = [
            "id",
            "name",
            "role",
            "image_url",
            "banner_url",
            "description",
            "difficulty",
            "playstyle_tags",
            "synergies",
            "counters",
            "countered_by",
            "video_url",
            "tips",
            "created_at",
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_banner_url(self, obj):
        return obj.banner.url if obj.banner else None

    def get_synergies(self, obj):
        return [
            {"id": hero.id, "name": hero.name, "role": hero.role, "image_url": hero.image.url if hero.image else None}
            for hero in obj.synergies.all()
        ]

    def get_counters(self, obj):
        return [
            {"id": hero.id, "name": hero.name, "role": hero.role, "image_url": hero.image.url if hero.image else None}
            for hero in obj.counters.all()
        ]

    def get_countered_by(self, obj):
        countered_by_heroes = Hero.objects.filter(counters=obj)
        return [
            {"id": hero.id, "name": hero.name, "role": hero.role, "image_url": hero.image.url if hero.image else None}
            for hero in countered_by_heroes
        ]
