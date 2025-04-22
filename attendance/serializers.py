from rest_framework import serializers
from .models import Shift, Attendance, LeaveType, LeaveRequest

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    shift_name = serializers.CharField(source='shift.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ('user', 'status', 'approved_by', 'rejection_reason')
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data