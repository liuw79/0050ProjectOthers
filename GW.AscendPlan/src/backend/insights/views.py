from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import datetime

from .models import InterviewTranscript, InsightAnalysis, AnalysisTemplate, AnalysisLog
from .serializers import (
    InterviewTranscriptSerializer, InterviewTranscriptCreateSerializer,
    InsightAnalysisSerializer, InsightAnalysisDetailSerializer,
    AnalysisTemplateSerializer, AnalysisLogSerializer, AnalysisLogDetailSerializer,
    CustomerInsightSummarySerializer, AnalysisRequestSerializer, ReviewInsightSerializer
)
from .services import InsightAnalysisService, AnalysisReportService
from appointments.models import Customer


class InterviewTranscriptViewSet(viewsets.ModelViewSet):
    """访谈文稿视图集"""
    queryset = InterviewTranscript.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer', 'interview_type']
    search_fields = ['title', 'customer__name', 'raw_transcript']
    ordering_fields = ['created_at', 'interview_date', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'create':
            return InterviewTranscriptCreateSerializer
        return InterviewTranscriptSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        queryset = InterviewTranscript.objects.select_related('customer', 'planner')
        
        # 如果不是超级用户，只显示自己的文稿
        if not self.request.user.is_superuser:
            queryset = queryset.filter(planner=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        """创建时自动设置规划师"""
        serializer.save(planner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """分析文稿"""
        transcript = self.get_object()
        
        if transcript.status == 'processing':
            return Response(
                {'error': '文稿正在处理中，请稍后再试'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AnalysisRequestSerializer(data={
            'transcript_id': transcript.id,
            'template_id': request.data.get('template_id')
        })
        
        if serializer.is_valid():
            try:
                service = InsightAnalysisService()
                insight = service.analyze_transcript(
                    transcript.id,
                    serializer.validated_data.get('template_id')
                )
                
                result_serializer = InsightAnalysisSerializer(insight)
                return Response(result_serializer.data)
                
            except Exception as e:
                return Response(
                    {'error': f'分析失败: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def analysis_result(self, request, pk=None):
        """获取分析结果"""
        transcript = self.get_object()
        
        try:
            insight = InsightAnalysis.objects.get(transcript=transcript)
            serializer = InsightAnalysisDetailSerializer(insight)
            return Response(serializer.data)
        except InsightAnalysis.DoesNotExist:
            return Response(
                {'error': '该文稿尚未分析'},
                status=status.HTTP_404_NOT_FOUND
            )


class InsightAnalysisViewSet(viewsets.ModelViewSet):
    """洞察分析视图集"""
    queryset = InsightAnalysis.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_reviewed', 'analysis_model', 'transcript__customer']
    search_fields = ['summary', 'recommendations', 'transcript__title', 'transcript__customer__name']
    ordering_fields = ['created_at', 'confidence_score', 'reviewed_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'retrieve':
            return InsightAnalysisDetailSerializer
        return InsightAnalysisSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        queryset = InsightAnalysis.objects.select_related(
            'transcript__customer', 'transcript__planner', 'reviewer'
        )
        
        # 如果不是超级用户，只显示自己的分析
        if not self.request.user.is_superuser:
            queryset = queryset.filter(transcript__planner=self.request.user)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """审核洞察分析"""
        insight = self.get_object()
        serializer = ReviewInsightSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            
            insight.is_reviewed = True
            insight.reviewer = request.user
            insight.reviewed_at = timezone.now()
            insight.review_notes = data.get('review_notes', '')
            
            # 如果有修正内容，更新相应字段
            if data.get('corrected_summary'):
                insight.summary = data['corrected_summary']
            if data.get('corrected_recommendations'):
                insight.recommendations = data['corrected_recommendations']
            if data.get('corrected_next_steps'):
                insight.next_steps = data['corrected_next_steps']
            
            insight.save()
            
            result_serializer = InsightAnalysisDetailSerializer(insight)
            return Response(result_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取分析统计信息"""
        queryset = self.get_queryset()
        
        stats = {
            'total_analysis': queryset.count(),
            'reviewed_count': queryset.filter(is_reviewed=True).count(),
            'pending_review': queryset.filter(is_reviewed=False).count(),
            'avg_confidence': queryset.aggregate(avg=Avg('confidence_score'))['avg'],
            'model_distribution': list(
                queryset.values('analysis_model')
                .annotate(count=Count('id'))
                .order_by('-count')
            )
        }
        
        return Response(stats)


class AnalysisTemplateViewSet(viewsets.ModelViewSet):
    """分析模板视图集"""
    queryset = AnalysisTemplate.objects.all()
    serializer_class = AnalysisTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'version']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name', 'version']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """创建时自动设置创建者"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """激活模板"""
        template = self.get_object()
        template.is_active = True
        template.save()
        
        serializer = self.get_serializer(template)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """停用模板"""
        template = self.get_object()
        template.is_active = False
        template.save()
        
        serializer = self.get_serializer(template)
        return Response(serializer.data)


class AnalysisLogViewSet(viewsets.ReadOnlyModelViewSet):
    """分析日志视图集（只读）"""
    queryset = AnalysisLog.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'template']
    search_fields = ['transcript__title', 'transcript__customer__name']
    ordering_fields = ['created_at', 'duration_seconds', 'estimated_cost']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'retrieve':
            return AnalysisLogDetailSerializer
        return AnalysisLogSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        queryset = AnalysisLog.objects.select_related(
            'transcript__customer', 'transcript__planner', 'template'
        )
        
        # 如果不是超级用户，只显示自己的日志
        if not self.request.user.is_superuser:
            queryset = queryset.filter(transcript__planner=self.request.user)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取日志统计信息"""
        queryset = self.get_queryset()
        
        stats = {
            'total_requests': queryset.count(),
            'success_count': queryset.filter(status='success').count(),
            'error_count': queryset.filter(status='error').count(),
            'timeout_count': queryset.filter(status='timeout').count(),
            'avg_duration': queryset.aggregate(avg=Avg('duration_seconds'))['avg'],
            'total_cost': queryset.aggregate(total=Avg('estimated_cost'))['total'] or 0,
            'daily_requests': list(
                queryset.extra({
                    'date': "DATE(created_at)"
                }).values('date').annotate(
                    count=Count('id')
                ).order_by('-date')[:7]
            )
        }
        
        return Response(stats)


class CustomerInsightViewSet(viewsets.ViewSet):
    """客户洞察视图集"""
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """获取客户洞察摘要列表"""
        # 构建查询集
        customers = Customer.objects.annotate(
            total_transcripts=Count('interviewtranscript'),
            completed_analysis=Count(
                'interviewtranscript__insightanalysis',
                filter=Q(interviewtranscript__status='completed')
            )
        ).filter(total_transcripts__gt=0)
        
        # 如果不是超级用户，只显示自己的客户
        if not request.user.is_superuser:
            customers = customers.filter(interviewtranscript__planner=request.user).distinct()
        
        # 构建摘要数据
        summaries = []
        for customer in customers:
            # 获取最新分析日期
            latest_analysis = InsightAnalysis.objects.filter(
                transcript__customer=customer
            ).order_by('-created_at').first()
            
            # 获取平均置信度
            avg_confidence = InsightAnalysis.objects.filter(
                transcript__customer=customer,
                confidence_score__isnull=False
            ).aggregate(avg=Avg('confidence_score'))['avg']
            
            # 统计关键洞察数量
            key_insights_count = InsightAnalysis.objects.filter(
                transcript__customer=customer,
                summary__isnull=False
            ).exclude(summary='').count()
            
            summaries.append({
                'customer_id': customer.id,
                'customer_name': customer.name,
                'total_transcripts': customer.total_transcripts,
                'completed_analysis': customer.completed_analysis,
                'latest_analysis_date': latest_analysis.created_at if latest_analysis else None,
                'key_insights_count': key_insights_count,
                'avg_confidence_score': avg_confidence
            })
        
        serializer = CustomerInsightSummarySerializer(summaries, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """获取特定客户的详细洞察报告"""
        try:
            service = AnalysisReportService()
            report = service.generate_customer_report(pk)
            return Response(report)
        except Customer.DoesNotExist:
            return Response(
                {'error': '客户不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'生成报告失败: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )