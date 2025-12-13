from django.contrib import admin
from .models import Hero

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'difficulty', 'created_at']
    list_filter = ['role', 'difficulty']
    search_fields = ['name', 'description']
    filter_horizontal = ['synergies', 'counters']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'role', 'image', 'description', 'difficulty')
        }),
        ('Analysis Data', {
            'fields': ('playstyle_tags', 'synergies', 'counters')
        }),
        ('Content (For Later)', {
            'fields': ('video_url', 'tips'),
            'classes': ('collapse',)
        }),
    )