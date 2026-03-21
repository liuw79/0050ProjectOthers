from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, Appointment, AppointmentNote


class CustomerSerializer(serializers.ModelSerializer):
    """客户序列化器"""
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_phone(self, value):
        """验证手机号唯一性"""
        if self.instance and self.instance.phone == value:
            return value
        
        if Customer.objects.filter(phone=value).exists():
            raise serializers.ValidationError("该手机号已被注册")
        return value


class PlannerSerializer(serializers.ModelSerializer):
    """规划师序列化器"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class AppointmentSerializer(serializers.ModelSerializer):
    """预约序列化器"""
    customer_info = CustomerSerializer(source='customer', read_only=True)
    planner_info = PlannerSerializer(source='planner', read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate(self, data):
        """验证预约时间冲突"""
        planner = data.get('planner')
        scheduled_date = data.get('scheduled_date')
        scheduled_time = data.get('scheduled_time')
        
        if planner and scheduled_date and scheduled_time:
            # 检查是否有时间冲突
            existing_appointments = Appointment.objects.filter(
                planner=planner,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                status__in=['pending', 'confirmed']
            )
            
            # 如果是更新操作，排除当前实例
            if self.instance:
                existing_appointments = existing_appointments.exclude(id=self.instance.id)
            
            if existing_appointments.exists():
                raise serializers.ValidationError("该时间段已有预约，请选择其他时间")
        
        return data


class AppointmentCreateSerializer(serializers.ModelSerializer):
    """创建预约的序列化器"""
    
    class Meta:
        model = Appointment
        fields = (
            'customer', 'planner', 'appointment_type', 'scheduled_date', 
            'scheduled_time', 'duration', 'location', 'meeting_link', 
            'purpose', 'preparation_notes'
        )
    
    def validate(self, data):
        """验证预约时间冲突"""
        planner = data.get('planner')
        scheduled_date = data.get('scheduled_date')
        scheduled_time = data.get('scheduled_time')
        
        if planner and scheduled_date and scheduled_time:
            # 检查是否有时间冲突
            existing_appointments = Appointment.objects.filter(
                planner=planner,
                scheduled_date=scheduled_date,
                scheduled_time=scheduled_time,
                status__in=['pending', 'confirmed']
            )
            
            if existing_appointments.exists():
                raise serializers.ValidationError("该时间段已有预约，请选择其他时间")
        
        return data


class AppointmentNoteSerializer(serializers.ModelSerializer):
    """预约记录序列化器"""
    appointment_info = AppointmentSerializer(source='appointment', read_only=True)
    
    class Meta:
        model = AppointmentNote
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class AppointmentListSerializer(serializers.ModelSerializer):
    """预约列表序列化器（简化版）"""
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    planner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = (
            'id', 'customer_name', 'customer_phone', 'planner_name',
            'appointment_type', 'scheduled_date', 'scheduled_time', 
            'duration', 'status', 'created_at'
        )
    
    def get_planner_name(self, obj):
        """获取规划师姓名"""
        if obj.planner.first_name or obj.planner.last_name:
            return f"{obj.planner.first_name} {obj.planner.last_name}".strip()
        return obj.planner.username