from rest_framework import serializers
from ..models import Account


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'first_name',
                  'last_name', 'email', 'is_staff',
                  'is_active', 'date_joined', 'profile_picture']
