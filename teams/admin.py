from django.contrib import admin
from .models import Team, TeamMember, Vote, Comment

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 6
    max_num = 6

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'composition_score', 'upvote_count', 'views', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['slug', 'views', 'created_at', 'updated_at']
    inlines = [TeamMemberInline]
    
    fieldsets = (
        ('Team Info', {
            'fields': ('user', 'name', 'description', 'slug')
        }),
        ('Analysis', {
            'fields': ('composition_score', 'analysis_data'),
            'classes': ('collapse',)
        }),
        ('Stats', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'team__name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'text_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'team__name', 'text']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'