from rest_framework import viewsets
from ..models import Account
from .serializers import AccountsSerializer


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountsSerializer