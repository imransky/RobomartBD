from rest_framework import serializers


from .models import Sell
from Basic_Api.serializers import ProductSerializer


class AdminPageSerializer(serializers.Serializer):
    total_order = serializers.IntegerField()
    active_order = serializers.IntegerField()
    pending_order = serializers.IntegerField()
    completed_order = serializers.IntegerField()
    success = serializers.IntegerField()

    current_month_sell = serializers.IntegerField()
    current_month_profit = serializers.IntegerField()
    total_sell = serializers.IntegerField()
    total_profit = serializers.IntegerField()


class AdminPage():
    def __init__(self,total_order  = None, active_order = None, pending_order = None, completed_order  = None,success = None,current_month_sell = None,current_month_profit = None,total_sell = None,total_profit = None):
        self.total_order = total_order
        self.active_order = active_order
        self.completed_order = completed_order
        self.success = success
        self.pending_order = pending_order
        self.current_month_sell = current_month_sell
        self.current_month_profit = current_month_profit
        self.total_sell = total_sell
        self.total_profit = total_profit



class AdminDashbordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sell
        fields = '__all__'

class YearlySellReport():
    def __init__(self,month = None, sell=None,profit = None):
        self.month = month
        self.sell = sell
        self.profit = profit

class YearlySellReportSerializer(serializers.Serializer):

    month = serializers.CharField()
    sell = serializers.IntegerField()
    profit = serializers.IntegerField()



