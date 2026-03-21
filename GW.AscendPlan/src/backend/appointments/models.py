from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Customer(models.Model):
    """客户信息模型"""
    name = models.CharField('客户姓名', max_length=100)
    phone_regex = RegexValidator(
        regex=r'^1[3-9]\d{9}$',
        message="手机号格式不正确"
    )
    phone = models.CharField('手机号', validators=[phone_regex], max_length=11, unique=True)
    email = models.EmailField('邮箱', blank=True, null=True)
    wechat = models.CharField('微信号', max_length=50, blank=True, null=True)
    age = models.PositiveIntegerField('年龄', blank=True, null=True)
    gender = models.CharField('性别', max_length=10, choices=[
        ('male', '男'),
        ('female', '女'),
        ('other', '其他')
    ], blank=True, null=True)
    education_background = models.CharField('教育背景', max_length=200, blank=True, null=True)
    current_situation = models.TextField('当前情况', blank=True, null=True)
    goals = models.TextField('学习目标', blank=True, null=True)
    notes = models.TextField('备注', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.phone})"


class Appointment(models.Model):
    """预约信息模型"""
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('rescheduled', '已改期')
    ]
    
    TYPE_CHOICES = [
        ('consultation', '咨询访谈'),
        ('planning', '规划制定'),
        ('review', '方案回顾'),
        ('follow_up', '跟进辅导')
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    planner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='规划师')
    
    appointment_type = models.CharField('预约类型', max_length=20, choices=TYPE_CHOICES)
    scheduled_date = models.DateField('预约日期')
    scheduled_time = models.TimeField('预约时间')
    duration = models.PositiveIntegerField('预计时长(分钟)', default=60)
    
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    location = models.CharField('地点', max_length=200, blank=True, null=True)
    meeting_link = models.URLField('会议链接', blank=True, null=True)
    
    purpose = models.TextField('预约目的', blank=True, null=True)
    preparation_notes = models.TextField('准备事项', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '预约'
        verbose_name_plural = '预约'
        ordering = ['scheduled_date', 'scheduled_time']
        unique_together = ['planner', 'scheduled_date', 'scheduled_time']
    
    def __str__(self):
        return f"{self.customer.name} - {self.scheduled_date} {self.scheduled_time}"


class AppointmentNote(models.Model):
    """预约记录模型"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, verbose_name='预约')
    
    actual_start_time = models.DateTimeField('实际开始时间', blank=True, null=True)
    actual_end_time = models.DateTimeField('实际结束时间', blank=True, null=True)
    
    interview_transcript = models.TextField('访谈记录', blank=True, null=True)
    key_findings = models.TextField('关键发现', blank=True, null=True)
    recommendations = models.TextField('建议事项', blank=True, null=True)
    next_steps = models.TextField('后续行动', blank=True, null=True)
    
    customer_satisfaction = models.PositiveIntegerField(
        '客户满意度', 
        choices=[(i, f'{i}分') for i in range(1, 6)],
        blank=True, 
        null=True
    )
    
    planner_notes = models.TextField('规划师备注', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '预约记录'
        verbose_name_plural = '预约记录'
    
    def __str__(self):
        return f"{self.appointment} - 记录"