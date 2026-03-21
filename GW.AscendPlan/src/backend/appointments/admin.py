from django.contrib import admin
from .models import Customer, Appointment, AppointmentNote


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """客户管理后台"""
    list_display = ('name', 'phone', 'email', 'age', 'gender', 'created_at')
    list_filter = ('gender', 'age', 'created_at')
    search_fields = ('name', 'phone', 'email', 'wechat')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'phone', 'email', 'wechat')
        }),
        ('个人信息', {
            'fields': ('age', 'gender', 'education_background')
        }),
        ('学习信息', {
            'fields': ('current_situation', 'goals')
        }),
        ('其他', {
            'fields': ('notes', 'created_at', 'updated_at')
        })
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """预约管理后台"""
    list_display = (
        'customer', 'planner', 'appointment_type', 'scheduled_date', 
        'scheduled_time', 'status', 'created_at'
    )
    list_filter = ('status', 'appointment_type', 'scheduled_date', 'planner')
    search_fields = ('customer__name', 'customer__phone', 'purpose')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('预约信息', {
            'fields': ('customer', 'planner', 'appointment_type', 'status')
        }),
        ('时间安排', {
            'fields': ('scheduled_date', 'scheduled_time', 'duration')
        }),
        ('地点信息', {
            'fields': ('location', 'meeting_link')
        }),
        ('详细信息', {
            'fields': ('purpose', 'preparation_notes')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤查询集"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(planner=request.user)


@admin.register(AppointmentNote)
class AppointmentNoteAdmin(admin.ModelAdmin):
    """预约记录管理后台"""
    list_display = (
        'appointment', 'actual_start_time', 'actual_end_time', 
        'customer_satisfaction', 'created_at'
    )
    list_filter = ('customer_satisfaction', 'created_at')
    search_fields = ('appointment__customer__name', 'key_findings', 'recommendations')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('预约信息', {
            'fields': ('appointment',)
        }),
        ('时间记录', {
            'fields': ('actual_start_time', 'actual_end_time')
        }),
        ('访谈内容', {
            'fields': ('interview_transcript', 'key_findings', 'recommendations', 'next_steps')
        }),
        ('评价与备注', {
            'fields': ('customer_satisfaction', 'planner_notes')
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤查询集"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(appointment__planner=request.user)