from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import F
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Team, Vote
from .pagination import TeamPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    TeamListSerializer,
    TeamDetailSerializer,
    TeamCreateSerializer,
    CommentSerializer,
)
import logging

logger = logging.getLogger(__name__)

class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for teams
    """
    queryset = (
        Team.objects.all()
        .select_related('user')
        .prefetch_related('members__hero')
    )

    # ...

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = TeamPagination
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return TeamCreateSerializer
        elif self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamListSerializer
    
    def get_queryset(self):
        from django.db.models import Count
        queryset = self.queryset
        
        # Filter by user
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Order by popularity or newest
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering == 'popular':
            # Annotate with vote count and order by it
            queryset = queryset.annotate(vote_count=Count('votes')).order_by(
                '-vote_count',
                '-views',
            )
        else:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when team is viewed"""
        instance = self.get_object()
        Team.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        instance.refresh_from_db(fields=['views'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Set the authenticated user when creating a team"""
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def vote(self, request, slug=None):
        """Toggle vote on a team"""
        team = self.get_object()
        user = request.user
        
        vote, created = Vote.objects.get_or_create(user=user, team=team)
        
        if not created:
            # User already voted, remove vote
            vote.delete()
            return Response({'voted': False, 'upvotes': team.upvote_count})
        
        return Response({'voted': True, 'upvotes': team.upvote_count})
    
    @action(
        detail=True,
        methods=['get', 'post'],
        permission_classes=[IsAuthenticatedOrReadOnly],
    )
    def comments(self, request, slug=None):
        """Get or create comments for a team"""
        team = self.get_object()
        
        if request.method == 'GET':
            comments = team.comments.all()
            serializer = CommentSerializer(
                comments,
                many=True,
                context={'request': request},
            )
            return Response(serializer.data)
        
        # POST - create comment
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            comment = serializer.save(user=request.user, team=team)
            response_serializer = CommentSerializer(
                comment,
                context={'request': request},
            )
            
            try:
                self._broadcast_comment(team.slug, response_serializer.data)
            except Exception:
                logger.exception("Comment broadcast failed (Redis/Channels). Comment saved anyway.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def my_teams(self, request):
        """Get current user's teams"""
        teams = self.queryset.filter(user=request.user)
        serializer = TeamListSerializer(teams, many=True)
        return Response(serializer.data)

    @staticmethod
    def _broadcast_comment(slug, payload):
        """Notify connected websocket clients about the new comment."""
        channel_layer = get_channel_layer()
        if not channel_layer:
            return
        async_to_sync(channel_layer.group_send)(
            f"team_comments_{slug}",
            {
                "type": "comment.broadcast",
                "comment": payload,
            },
        )
