from django.db import models
from django.contrib.auth.models import User
from appointments.models import Customer


class InterviewTranscript(models.Model):
    """访谈文稿模型"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    planner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='规划师')
    
    title = models.CharField('标题', max_length=200)
    raw_transcript = models.TextField('原始文稿')
    
    # 处理状态
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('failed', '处理失败')
    ]
    status = models.CharField('处理状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 元数据
    interview_date = models.DateField('访谈日期', blank=True, null=True)
    duration_minutes = models.PositiveIntegerField('时长(分钟)', blank=True, null=True)
    interview_type = models.CharField('访谈类型', max_length=50, blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '访谈文稿'
        verbose_name_plural = '访谈文稿'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.name} - {self.title}"


class InsightAnalysis(models.Model):
    """洞察分析结果模型"""
    transcript = models.OneToOneField(
        InterviewTranscript, 
        on_delete=models.CASCADE, 
        verbose_name='访谈文稿'
    )
    
    # LLM 分析结果
    key_information = models.JSONField('关键信息提取', default=dict, blank=True)
    learning_goals = models.JSONField('学习目标分析', default=dict, blank=True)
    current_situation = models.JSONField('现状分析', default=dict, blank=True)
    challenges_obstacles = models.JSONField('挑战与障碍', default=dict, blank=True)
    strengths_resources = models.JSONField('优势与资源', default=dict, blank=True)
    
    # 结构化洞察
    summary = models.TextField('总结概述', blank=True, null=True)
    recommendations = models.TextField('初步建议', blank=True, null=True)
    next_steps = models.TextField('后续行动建议', blank=True, null=True)
    
    # 分析元数据
    analysis_model = models.CharField('使用模型', max_length=50, blank=True, null=True)
    analysis_version = models.CharField('分析版本', max_length=20, default='1.0')
    confidence_score = models.FloatField('置信度分数', blank=True, null=True)
    
    # 人工审核
    is_reviewed = models.BooleanField('已人工审核', default=False)
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_insights',
        verbose_name='审核人'
    )
    review_notes = models.TextField('审核备注', blank=True, null=True)
    reviewed_at = models.DateTimeField('审核时间', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '洞察分析'
        verbose_name_plural = '洞察分析'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transcript.customer.name} - 洞察分析"


class AnalysisTemplate(models.Model):
    """分析模板模型"""
    name = models.CharField('模板名称', max_length=100)
    description = models.TextField('模板描述', blank=True, null=True)
    
    # Prompt 模板
    system_prompt = models.TextField('系统提示词')
    user_prompt_template = models.TextField('用户提示词模板')
    
    # 模板配置
    target_fields = models.JSONField('目标字段配置', default=list)
    model_config = models.JSONField('模型配置', default=dict)
    
    # 模板状态
    is_active = models.BooleanField('是否启用', default=True)
    version = models.CharField('版本号', max_length=20, default='1.0')
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '分析模板'
        verbose_name_plural = '分析模板'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} (v{self.version})"


class AnalysisLog(models.Model):
    """分析日志模型"""
    transcript = models.ForeignKey(
        InterviewTranscript, 
        on_delete=models.CASCADE, 
        verbose_name='访谈文稿'
    )
    template = models.ForeignKey(
        AnalysisTemplate, 
        on_delete=models.SET_NULL, 
        null=True, 
        verbose_name='使用模板'
    )
    
    # 请求信息
    request_data = models.JSONField('请求数据', default=dict)
    response_data = models.JSONField('响应数据', default=dict)
    
    # 执行信息
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间', blank=True, null=True)
    duration_seconds = models.FloatField('执行时长(秒)', blank=True, null=True)
    
    # 结果状态
    STATUS_CHOICES = [
        ('success', '成功'),
        ('error', '错误'),
        ('timeout', '超时')
    ]
    status = models.CharField('执行状态', max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField('错误信息', blank=True, null=True)
    
    # 成本信息
    token_usage = models.JSONField('Token使用量', default=dict, blank=True)
    estimated_cost = models.DecimalField('预估成本', max_digits=10, decimal_places=4, blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '分析日志'
        verbose_name_plural = '分析日志'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transcript.customer.name} - {self.status} - {self.created_at}"