from django.db import models
from django.contrib.auth.models import User
from heroes.models import Hero
import uuid

class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # For sharing - unique URL slug
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Social features
    views = models.IntegerField(default=0)
    
    # Analysis results (cached)
    analysis_data = models.JSONField(default=dict, blank=True)
    composition_score = models.IntegerField(default=0, help_text="Overall score 0-100")
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not exists
        if not self.slug:
            self.slug = f"{self.name[:30].lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"
    
    @property
    def upvote_count(self):
        return self.votes.count()


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    position = models.IntegerField(help_text="Position in team (1-6)")
    
    class Meta:
        ordering = ['position']
        unique_together = ['team', 'position']
        constraints = [
            models.CheckConstraint(
                check=models.Q(position__gte=1) & models.Q(position__lte=6),
                name='valid_position'
            )
        ]
    
    def __str__(self):
        return f"{self.hero.name} in {self.team.name} (Pos {self.position})"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'team']  # One vote per user per team
    
    def __str__(self):
        return f"{self.user.username} voted for {self.team.name}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.team.name}"