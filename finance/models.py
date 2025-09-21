from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, choices=[("UZS", "So'm"), ("USD", "Dollar")], default="UZS")

    def __str__(self):
        return f"{self.user} - {self.name} ({self.currency})"


class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source_type = models.CharField(max_length=10, choices=[("cash", "Naqt"), ("card", "Karta"), ("usd", "Dollar")])
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.source_type})"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source_type = models.CharField(max_length=10, choices=[("cash", "Naqt"), ("card", "Karta"), ("usd", "Dollar")])
    card = models.ForeignKey(Card, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.source_type})"
