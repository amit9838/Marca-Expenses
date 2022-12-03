from django.urls import path
from . import views
from .views import ListExpense
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name = 'expenses'),
    path('expense-summary', views.expense_summary, name = 'expense-summary'),
    path('add-expense/', views.add_expense, name = 'add-expense'),
    path('edit-expense/<int:id>/', views.edit_expense, name = 'edit-expense'),
    path('delete-expense/<int:id>/', views.delete_expense, name = 'delete-expense'),
    path('search-expense/', csrf_exempt(views.search_expense), name = 'search-expense'),
    path('export-csv/', views.export_csv, name = 'export-csv'),
    path('list_expenses/', ListExpense.as_view(), name = 'list_expenses'),  # API View url
]
