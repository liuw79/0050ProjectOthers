from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import InterviewTranscript, InsightAnalysis, AnalysisTemplate, AnalysisLog


@admin.register(InterviewTranscript)
class InterviewTranscriptAdmin(admin.ModelAdmin):
    """访谈文稿管理"""
    list_display = [
        'title', 'customer', 'planner', 'interview_type', 
        'status', 'interview_date', 'created_at'
    ]
    list_filter = [
        'status', 'interview_type', 'interview_date', 
        'created_at', 'planner'
    ]
    search_fields = [
        'title', 'customer__name', 'customer__phone', 
        'planner__username', 'raw_transcript'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'interview_date'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'customer', 'planner', 'interview_type')
        }),
        ('访谈内容', {
            'fields': ('interview_date', 'duration_minutes', 'raw_transcript')
        }),
        ('状态信息', {
            'fields': ('status', 'notes')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """根据用户权限过滤查询集"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(planner=request.user)
    
    def save_model(self, request, obj, form, change):
        """保存时自动设置规划师"""
        if not change:  # 新建时
            obj.planner = request.user
        super().save_model(request, obj, form, change)


@admin.register(InsightAnalysis)
class InsightAnalysisAdmin(admin.ModelAdmin):
    """洞察分析管理"""
    list_display = [
        'transcript_link', 'customer_name', 'analysis_model',
        'confidence_score', 'is_reviewed', 'reviewer', 'created_at'
    ]
    list_filter = [
        'is_reviewed', 'analysis_model', 'created_at',
        'reviewed_at', 'transcript__planner'
    ]
    search_fields = [
        'transcript__title', 'transcript__customer__name',
        'summary', 'recommendations', 'reviewer__username'
    ]
    readonly_fields = [
        'created_at', 'updated_at', 'analysis_duration',
        'estimated_cost', 'raw_response'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('关联信息', {
            'fields': ('transcript',)
        }),
        ('分析结果', {
            'fields': (
                'summary', 'key_insights', 'recommendations', 
                'next_steps', 'confidence_score'
            )
        }),
        ('技术信息', {
            'fields': (
                'analysis_model', 'analysis_duration', 
                'estimated_cost', 'raw_response'
            ),
            'classes': ('collapse',)
        }),
        ('审核信息', {
            'fields': (
                'is_reviewed', 'reviewer', 'reviewed_at', 
                'review_notes'
            )
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def transcript_link(self, obj):
        """文稿链接"""
        url = reverse('admin:insights_interviewtranscript_change', args=[obj.transcript.id])
        return format_html('<a href="{}">{}</a>', url, obj.transcript.title)
    transcript_link.short_description = '访谈文稿'
    
    def customer_name(self, obj):
        """客户姓名"""
        return obj.transcript.customer.name
    customer_name.short_description = '客户'
    
    def get_queryset(self, request):
        """根据用户权限过滤查询集"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(transcript__planner=request.user)


@admin.register(AnalysisTemplate)
class AnalysisTemplateAdmin(admin.ModelAdmin):
    """分析模板管理"""
    list_display = [
        'name', 'version', 'is_active', 'created_by', 'created_at'
    ]
    list_filter = ['is_active', 'version', 'created_at', 'created_by']
    search_fields = ['name', 'description', 'prompt_template']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'version', 'is_active')
        }),
        ('模板内容', {
            'fields': ('prompt_template', 'expected_output_format')
        }),
        ('创建信息', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        """保存时自动设置创建者"""
        if not change:  # 新建时
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AnalysisLog)
class AnalysisLogAdmin(admin.ModelAdmin):
    """分析日志管理"""
    list_display = [
        'transcript_link', 'customer_name', 'template', 
        'status', 'duration_seconds', 'estimated_cost', 'created_at'
    ]
    list_filter = [
        'status', 'template', 'created_at', 
        'transcript__planner'
    ]
    search_fields = [
        'transcript__title', 'transcript__customer__name',
        'template__name', 'error_message'
    ]
    readonly_fields = [
        'transcript', 'template', 'status', 'duration_seconds',
        'estimated_cost', 'error_message', 'request_data',
        'response_data', 'created_at'
    ]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('关联信息', {
            'fields': ('transcript', 'template')
        }),
        ('执行结果', {
            'fields': ('status', 'duration_seconds', 'estimated_cost')
        }),
        ('错误信息', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('请求响应数据', {
            'fields': ('request_data', 'response_data'),
            'classes': ('collapse',)
        }),
        ('时间戳', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def transcript_link(self, obj):
        """文稿链接"""
        url = reverse('admin:insights_interviewtranscript_change', args=[obj.transcript.id])
        return format_html('<a href="{}">{}</a>', url, obj.transcript.title)
    transcript_link.short_description = '访谈文稿'
    
    def customer_name(self, obj):
        """客户姓名"""
        return obj.transcript.customer.name
    customer_name.short_description = '客户'
    
    def has_add_permission(self, request):
        """禁止手动添加日志"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """禁止修改日志"""
        return False
    
    def get_queryset(self, request):
        """根据用户权限过滤查询集"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(transcript__planner=request.user)