from django.db import models

class Hero(models.Model):
    ROLE_CHOICES = [
        ('VANGUARD', 'Vanguard'),    # Tanks
        ('DUELIST', 'Duelist'),      # DPS
        ('STRATEGIST', 'Strategist'), # Support
    ]
    
    # Basic info
    name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='heroes/', blank=True, null=True)
    banner = models.ImageField(upload_to='heroes/banners/', blank=True, null=True, help_text="Banner image for team showcase")
    description = models.TextField(blank=True)
    
    # For later - your YouTube videos
    video_url = models.URLField(blank=True, help_text="YouTube video URL")
    tips = models.TextField(blank=True, help_text="Your tips for this hero")
    
    # For analysis algorithm
    playstyle_tags = models.JSONField(
        default=list,
        help_text="Tags like: mobility, burst-damage, area-control, dive, poke"
    )
    
    # Synergies (heroes this works well with)
    synergies = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='synergy_with',
        blank=True,
        help_text="Heroes this hero has synergy with"
    )
    
    # Counters (heroes this hero beats)
    counters = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='countered_by',
        blank=True,
        help_text="Heroes this hero counters"
    )
    
    # Meta tracking
    difficulty = models.IntegerField(
        default=2,
        choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')],
        help_text="Difficulty to play (1-3)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"