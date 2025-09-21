from rest_framework import serializers
from .models import Card, Income, Expense, IncomeCategory, ExpenseCategory


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ["id", "name", "balance", "currency"]


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ["id", "name"]


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "name"]


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id", "category", "amount", "source_type", "card", "created_at"]


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "category", "amount", "source_type", "card", "created_at"]


class BalanceSerializer(serializers.Serializer):
    naqt = serializers.DecimalField(max_digits=12, decimal_places=2)
    karta = serializers.DecimalField(max_digits=12, decimal_places=2)
    dollar = serializers.DecimalField(max_digits=12, decimal_places=2)
    umumiy = serializers.DecimalField(max_digits=12, decimal_places=2)
