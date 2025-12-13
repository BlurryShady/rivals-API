from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Hero
from .serializers import HeroListSerializer, HeroDetailSerializer

class HeroViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for heroes
    List all heroes or retrieve a specific hero
    """
    queryset = Hero.objects.all().order_by('name')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'role', 'difficulty']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HeroDetailSerializer
        return HeroListSerializer
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """Filter heroes by role"""
        role = request.query_params.get('role', None)
        if role:
            heroes = self.queryset.filter(role=role.upper())
            serializer = HeroListSerializer(heroes, many=True)
            return Response(serializer.data)
        return Response({'error': 'Role parameter required'}, status=400)