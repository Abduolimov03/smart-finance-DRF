from django.urls import path
from .views import (
    CardAPIView, CardDetailAPIView,
    IncomeAPIView, IncomeDetailAPIView,
    ExpenseAPIView, ExpenseDetailAPIView,
    IncomeCategoryAPIView, IncomeCategoryDetailAPIView,
    ExpenseCategoryAPIView, ExpenseCategoryDetailAPIView,
    BalanceAPIView, TimeframeFilterAPIView, CalendarAPIView
)

urlpatterns = [
    # Card endpoints
    path('cards/', CardAPIView.as_view(), name='card-list-create'),
    path('cards/<int:pk>/', CardDetailAPIView.as_view(), name='card-detail'),

    # Income endpoints
    path('incomes/', IncomeAPIView.as_view(), name='income-list-create'),
    path('incomes/<int:pk>/', IncomeDetailAPIView.as_view(), name='income-detail'),

    # Expense endpoints
    path('expenses/', ExpenseAPIView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailAPIView.as_view(), name='expense-detail'),

    # Income category endpoints
    path('income-categories/', IncomeCategoryAPIView.as_view(), name='income-category-list-create'),
    path('income-categories/<int:pk>/', IncomeCategoryDetailAPIView.as_view(), name='income-category-detail'),

    # Expense category endpoints
    path('expense-categories/', ExpenseCategoryAPIView.as_view(), name='expense-category-list-create'),
    path('expense-categories/<int:pk>/', ExpenseCategoryDetailAPIView.as_view(), name='expense-category-detail'),

    # Balance endpoint
    path('balance/', BalanceAPIView.as_view(), name='balance'),

    # Timeframe filter
    path('balance/filter/', TimeframeFilterAPIView.as_view(), name='balance-timeframe-filter'),

    # Calendar view
    path('balance/calendar/', CalendarAPIView.as_view(), name='balance-calendar'),
]
