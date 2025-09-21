from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from django.db.models import Sum
from django.db import transaction
from datetime import datetime, timedelta

from .models import Card, Income, Expense, IncomeCategory, ExpenseCategory
from .serializers import (
    CardSerializer, IncomeSerializer, ExpenseSerializer,
    IncomeCategorySerializer, ExpenseCategorySerializer
)
from .filters import IncomeFilter, ExpenseFilter


class CardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cards = Card.objects.filter(user=request.user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Card.objects.get(pk=pk, user=self.request.user)
        except Card.DoesNotExist:
            raise serializers.ValidationError("Card topilmadi")

    def delete(self, request, pk):
        card = self.get_object(pk)
        card.delete()
        return Response({"msg": "Card o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)


class IncomeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        incomes = Income.objects.filter(user=request.user)
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        income = serializer.save(user=request.user)

        if income.source_type == "card" and income.card:
            income.card.balance += income.amount
            income.card.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncomeDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Income.objects.get(pk=pk, user=self.request.user)
        except Income.DoesNotExist:
            raise serializers.ValidationError("Income topilmadi")

    def get(self, request, pk):
        income_obj = self.get_object(pk)
        serializer = IncomeSerializer(income_obj)
        return Response(serializer.data)

    @transaction.atomic
    def put(self, request, pk):
        income_obj = self.get_object(pk)
        serializer = IncomeSerializer(income_obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        if income_obj.source_type == "card" and income_obj.card:
            income_obj.card.balance -= income_obj.amount
            income_obj.card.save()

        income = serializer.save(user=request.user)

        if income.source_type == "card" and income.card:
            income.card.balance += income.amount
            income.card.save()

        return Response(serializer.data)

    @transaction.atomic
    def patch(self, request, pk):
        income_obj = self.get_object(pk)
        serializer = IncomeSerializer(income_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if income_obj.source_type == "card" and income_obj.card:
            income_obj.card.balance -= income_obj.amount
            income_obj.card.save()

        income = serializer.save(user=request.user)

        if income.source_type == "card" and income.card:
            income.card.balance += income.amount
            income.card.save()

        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk):
        income = self.get_object(pk)
        if income.source_type == "card" and income.card:
            income.card.balance -= income.amount
            income.card.save()
        income.delete()
        return Response({"msg": "Income o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)


class ExpenseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)



    @transaction.atomic
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expense = serializer.save(user=request.user)

        if expense.source_type == "card" and expense.card:
            if expense.card.balance < expense.amount:
                raise serializers.ValidationError("Kartada mablag' yetarli emas")
            expense.card.balance -= expense.amount
            expense.card.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk, user=self.request.user)
        except Expense.DoesNotExist:
            raise serializers.ValidationError("Expense topilmadi")

    def get(self, request, pk):
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request, pk):
        expense_obj = self.get_object(pk)
        serializer = ExpenseSerializer(expense_obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        # eski summani qayta tiklash
        if expense_obj.source_type == "card" and expense_obj.card:
            expense_obj.card.balance += expense_obj.amount
            expense_obj.card.save()

        expense = serializer.save(user=request.user)

        if expense.source_type == "card" and expense.card:
            if expense.card.balance < expense.amount:
                raise serializers.ValidationError("Kartada mablag' yetarli emas")
            expense.card.balance -= expense.amount
            expense.card.save()

        return Response(serializer.data)

    @transaction.atomic
    def patch(self, request, pk):
        expense_obj = self.get_object(pk)
        serializer = ExpenseSerializer(expense_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # eski summani qayta tiklash
        if expense_obj.source_type == "card" and expense_obj.card:
            expense_obj.card.balance += expense_obj.amount
            expense_obj.card.save()

        expense = serializer.save(user=request.user)

        if expense.source_type == "card" and expense.card:
            if expense.card.balance < expense.amount:
                raise serializers.ValidationError("Kartada mablag' yetarli emas")
            expense.card.balance -= expense.amount
            expense.card.save()

        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk):
        expense = self.get_object(pk)
        if expense.source_type == "card" and expense.card:
            expense.card.balance += expense.amount
            expense.card.save()
        expense.delete()
        return Response({"msg": "Expense o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)


class IncomeCategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = IncomeCategory.objects.all()
        serializer = IncomeCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncomeCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IncomeCategoryDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return IncomeCategory.objects.get(pk=pk)
        except IncomeCategory.DoesNotExist:
            raise serializers.ValidationError("Category topilmadi")

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({"msg": "Category o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)


class ExpenseCategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = ExpenseCategory.objects.all()
        serializer = ExpenseCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExpenseCategoryDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return ExpenseCategory.objects.get(pk=pk)
        except ExpenseCategory.DoesNotExist:
            raise serializers.ValidationError("Category topilmadi")

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({"msg": "Category o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)


class BalanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        total_income = Income.objects.filter(user=user).aggregate(Sum("amount"))["amount__sum"] or 0
        total_expense = Expense.objects.filter(user=user).aggregate(Sum("amount"))["amount__sum"] or 0
        balance = total_income - total_expense
        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        })


class TimeframeFilterAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        filter_type = request.query_params.get("type", "daily")
        today = datetime.today()

        if filter_type == "daily":
            start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end = today
        elif filter_type == "weekly":
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
        elif filter_type == "monthly":
            start = today.replace(day=1)
            next_month = (today.month % 12) + 1
            year = today.year + (today.month // 12)
            end = datetime(year, next_month, 1) - timedelta(days=1)
        elif filter_type == "yearly":
            start = today.replace(month=1, day=1)
            end = today.replace(month=12, day=31)
        else:
            return Response({"error": "Noto‘g‘ri filter"}, status=status.HTTP_400_BAD_REQUEST)

        incomes = Income.objects.filter(user=user, created_at__date__range=[start, end])
        expenses = Expense.objects.filter(user=user, created_at__date__range=[start, end])

        total_income = incomes.aggregate(Sum("amount"))["amount__sum"] or 0
        total_expense = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
        balance = total_income - total_expense

        return Response({
            "filter_type": filter_type,
            "incomes": IncomeSerializer(incomes, many=True).data,
            "expenses": ExpenseSerializer(expenses, many=True).data,
            "summary": {"total_income": total_income, "total_expense": total_expense, "balance": balance}
        })


class CalendarAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        start_date = request.query_params.get("start")
        end_date = request.query_params.get("end")
        if not start_date or not end_date:
            return Response({"error": "start va end sanalarni yuboring"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Sana formati YYYY-MM-DD bo‘lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        incomes = Income.objects.filter(user=user, created_at__date__range=[start, end])
        expenses = Expense.objects.filter(user=user, created_at__date__range=[start, end])

        total_income = incomes.aggregate(Sum("amount"))["amount__sum"] or 0
        total_expense = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
        balance = total_income - total_expense

        return Response({
            "incomes": IncomeSerializer(incomes, many=True).data,
            "expenses": ExpenseSerializer(expenses, many=True).data,
            "summary": {"total_income": total_income, "total_expense": total_expense, "balance": balance}
        })
