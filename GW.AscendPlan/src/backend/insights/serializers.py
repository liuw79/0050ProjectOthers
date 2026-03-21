from rest_framework import serializers
from appointments.models import Customer
from .models import InterviewTranscript, InsightAnalysis, AnalysisTemplate, AnalysisLog


class InterviewTranscriptSerializer(serializers.ModelSerializer):
    """访谈文稿序列化器"""
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    planner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = InterviewTranscript
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'status')
    
    def get_planner_name(self, obj):
        """获取规划师姓名"""
        if obj.planner.first_name or obj.planner.last_name:
            return f"{obj.planner.first_name} {obj.planner.last_name}".strip()
        return obj.planner.username


class InterviewTranscriptCreateSerializer(serializers.ModelSerializer):
    """创建访谈文稿的序列化器"""
    
    class Meta:
        model = InterviewTranscript
        fields = (
            'customer', 'title', 'raw_transcript', 'interview_date', 
            'duration_minutes', 'interview_type'
        )
    
    def validate_raw_transcript(self, value):
        """验证文稿内容"""
        if len(value.strip()) < 50:
            raise serializers.ValidationError("文稿内容过短，至少需要50个字符")
        return value


class InsightAnalysisSerializer(serializers.ModelSerializer):
    """洞察分析序列化器"""
    transcript_info = InterviewTranscriptSerializer(source='transcript', read_only=True)
    reviewer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = InsightAnalysis
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_reviewer_name(self, obj):
        """获取审核人姓名"""
        if not obj.reviewer:
            return None
        if obj.reviewer.first_name or obj.reviewer.last_name:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}".strip()
        return obj.reviewer.username


class InsightAnalysisDetailSerializer(serializers.ModelSerializer):
    """洞察分析详情序列化器"""
    transcript = InterviewTranscriptSerializer(read_only=True)
    reviewer_name = serializers.SerializerMethodField()
    
    # 结构化字段的友好显示
    key_info_summary = serializers.SerializerMethodField()
    goals_summary = serializers.SerializerMethodField()
    challenges_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = InsightAnalysis
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_reviewer_name(self, obj):
        """获取审核人姓名"""
        if not obj.reviewer:
            return None
        if obj.reviewer.first_name or obj.reviewer.last_name:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}".strip()
        return obj.reviewer.username
    
    def get_key_info_summary(self, obj):
        """获取关键信息摘要"""
        if isinstance(obj.key_information, dict):
            return obj.key_information.get('summary', '')
        return ''
    
    def get_goals_summary(self, obj):
        """获取目标摘要"""
        if isinstance(obj.learning_goals, dict):
            return obj.learning_goals.get('summary', '')
        return ''
    
    def get_challenges_summary(self, obj):
        """获取挑战摘要"""
        if isinstance(obj.challenges_obstacles, dict):
            return obj.challenges_obstacles.get('summary', '')
        return ''


class AnalysisTemplateSerializer(serializers.ModelSerializer):
    """分析模板序列化器"""
    created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalysisTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')
    
    def get_created_by_name(self, obj):
        """获取创建者姓名"""
        if obj.created_by.first_name or obj.created_by.last_name:
            return f"{obj.created_by.first_name} {obj.created_by.last_name}".strip()
        return obj.created_by.username


class AnalysisLogSerializer(serializers.ModelSerializer):
    """分析日志序列化器"""
    transcript_title = serializers.CharField(source='transcript.title', read_only=True)
    customer_name = serializers.CharField(source='transcript.customer.name', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = AnalysisLog
        fields = (
            'id', 'transcript_title', 'customer_name', 'template_name',
            'status', 'duration_seconds', 'estimated_cost', 'error_message',
            'created_at'
        )
        read_only_fields = ('created_at',)


class AnalysisLogDetailSerializer(serializers.ModelSerializer):
    """分析日志详情序列化器"""
    transcript = InterviewTranscriptSerializer(read_only=True)
    template = AnalysisTemplateSerializer(read_only=True)
    
    class Meta:
        model = AnalysisLog
        fields = '__all__'
        read_only_fields = ('created_at',)


class CustomerInsightSummarySerializer(serializers.Serializer):
    """客户洞察摘要序列化器"""
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField()
    total_transcripts = serializers.IntegerField()
    completed_analysis = serializers.IntegerField()
    latest_analysis_date = serializers.DateTimeField(allow_null=True)
    key_insights_count = serializers.IntegerField()
    avg_confidence_score = serializers.FloatField(allow_null=True)


class AnalysisRequestSerializer(serializers.Serializer):
    """分析请求序列化器"""
    transcript_id = serializers.IntegerField()
    template_id = serializers.IntegerField(required=False)
    
    def validate_transcript_id(self, value):
        """验证文稿ID"""
        try:
            transcript = InterviewTranscript.objects.get(id=value)
            if transcript.status == 'processing':
                raise serializers.ValidationError("该文稿正在处理中，请稍后再试")
        except InterviewTranscript.DoesNotExist:
            raise serializers.ValidationError("文稿不存在")
        return value
    
    def validate_template_id(self, value):
        """验证模板ID"""
        if value:
            try:
                template = AnalysisTemplate.objects.get(id=value, is_active=True)
            except AnalysisTemplate.DoesNotExist:
                raise serializers.ValidationError("模板不存在或已禁用")
        return value


class ReviewInsightSerializer(serializers.Serializer):
    """审核洞察序列化器"""
    is_approved = serializers.BooleanField()
    review_notes = serializers.CharField(required=False, allow_blank=True)
    
    # 可选的修正字段
    corrected_summary = serializers.CharField(required=False, allow_blank=True)
    corrected_recommendations = serializers.CharField(required=False, allow_blank=True)
    corrected_next_steps = serializers.CharField(required=False, allow_blank=True)