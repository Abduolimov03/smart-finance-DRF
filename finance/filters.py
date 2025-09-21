import django_filters
from .models import Income, Expense
from django.utils.timezone import now, timedelta


class IncomeFilter(django_filters.FilterSet):
    timeframe = django_filters.CharFilter(method="filter_by_timeframe")

    class Meta:
        model = Income
        fields = ["timeframe"]

    def filter_by_timeframe(self, queryset, name, value):
        today = now().date()
        if value == "daily":
            return queryset.filter(created_at__date=today)
        elif value == "weekly":
            start = today - timedelta(days=today.weekday())
            return queryset.filter(created_at__date__gte=start)
        elif value == "monthly":
            return queryset.filter(created_at__month=today.month, created_at__year=today.year)
        elif value == "yearly":
            return queryset.filter(created_at__year=today.year)
        return queryset


class ExpenseFilter(django_filters.FilterSet):
    timeframe = django_filters.CharFilter(method="filter_by_timeframe")

    class Meta:
        model = Expense
        fields = ["timeframe"]

    def filter_by_timeframe(self, queryset, name, value):
        today = now().date()
        if value == "daily":
            return queryset.filter(created_at__date=today)
        elif value == "weekly":
            start = today - timedelta(days=today.weekday())
            return queryset.filter(created_at__date__gte=start)
        elif value == "monthly":
            return queryset.filter(created_at__month=today.month, created_at__year=today.year)
        elif value == "yearly":
            return queryset.filter(created_at__year=today.year)
        return queryset
