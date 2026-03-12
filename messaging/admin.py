from django.contrib import admin
from .models import Conversation, Message, Report


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'created_at', 'updated_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'conversation', 'is_read', 'created_at']
    list_filter = ['is_read']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'reporter', 'reported_user', 'reason', 'is_resolved', 'created_at']
    list_filter = ['reason', 'is_resolved']
    actions = ['resolve_reports']

    @admin.action(description='Mark selected reports as resolved')
    def resolve_reports(self, request, queryset):
        queryset.update(is_resolved=True)
