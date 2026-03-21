from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime, date

from .models import Customer, Appointment, AppointmentNote
from .serializers import (
    CustomerSerializer, AppointmentSerializer, AppointmentCreateSerializer,
    AppointmentNoteSerializer, AppointmentListSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    """客户管理视图集"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'age']
    search_fields = ['name', 'phone', 'email', 'wechat']
    ordering_fields = ['created_at', 'name', 'age']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """获取客户的所有预约"""
        customer = self.get_object()
        appointments = Appointment.objects.filter(customer=customer)
        serializer = AppointmentListSerializer(appointments, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    """预约管理视图集"""
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'appointment_type', 'planner', 'scheduled_date']
    search_fields = ['customer__name', 'customer__phone', 'purpose']
    ordering_fields = ['scheduled_date', 'scheduled_time', 'created_at']
    ordering = ['scheduled_date', 'scheduled_time']
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'create':
            return AppointmentCreateSerializer
        elif self.action == 'list':
            return AppointmentListSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        queryset = Appointment.objects.select_related('customer', 'planner')
        
        # 如果不是超级用户，只显示自己的预约
        if not self.request.user.is_superuser:
            queryset = queryset.filter(planner=self.request.user)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """获取今日预约"""
        today = date.today()
        appointments = self.get_queryset().filter(scheduled_date=today)
        serializer = AppointmentListSerializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """获取即将到来的预约"""
        today = date.today()
        appointments = self.get_queryset().filter(
            scheduled_date__gte=today,
            status__in=['pending', 'confirmed']
        ).order_by('scheduled_date', 'scheduled_time')[:10]
        serializer = AppointmentListSerializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """确认预约"""
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消预约"""
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成预约"""
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        """获取可用时间段"""
        planner_id = request.query_params.get('planner_id')
        date_str = request.query_params.get('date')
        
        if not planner_id or not date_str:
            return Response(
                {'error': '请提供规划师ID和日期'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': '日期格式错误，请使用YYYY-MM-DD格式'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取该日期已预约的时间段
        booked_slots = Appointment.objects.filter(
            planner_id=planner_id,
            scheduled_date=target_date,
            status__in=['pending', 'confirmed']
        ).values_list('scheduled_time', flat=True)
        
        # 定义工作时间段（9:00-18:00，每小时一个时间段）
        all_slots = [
            '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00'
        ]
        
        # 过滤掉已预约的时间段
        available_slots = [
            slot for slot in all_slots 
            if slot not in [t.strftime('%H:%M') for t in booked_slots]
        ]
        
        return Response({'available_slots': available_slots})


class AppointmentNoteViewSet(viewsets.ModelViewSet):
    """预约记录视图集"""
    queryset = AppointmentNote.objects.all()
    serializer_class = AppointmentNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['appointment__status', 'customer_satisfaction']
    search_fields = ['key_findings', 'recommendations', 'planner_notes']
    
    def get_queryset(self):
        """根据用户权限过滤查询集"""
        queryset = AppointmentNote.objects.select_related('appointment__customer', 'appointment__planner')
        
        # 如果不是超级用户，只显示自己的预约记录
        if not self.request.user.is_superuser:
            queryset = queryset.filter(appointment__planner=self.request.user)
        
        return queryset