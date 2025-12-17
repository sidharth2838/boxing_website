from django.contrib import admin
from .models import BoxingFAQ, ChatHistory, TrainingSchedule, MembershipPlan

@admin.register(BoxingFAQ)
class BoxingFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer', 'keywords']

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_message', 'is_boxing_related', 'created_at']
    list_filter = ['is_boxing_related', 'created_at']
    search_fields = ['user_message', 'bot_response']
    readonly_fields = ['created_at']

@admin.register(TrainingSchedule)
class TrainingScheduleAdmin(admin.ModelAdmin):
    list_display = ['day', 'time_slot', 'class_type', 'coach', 'available_slots']
    list_filter = ['day', 'class_type']

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_active']
    list_filter = ['is_active']