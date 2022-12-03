from datetime import datetime
from urllib import request
from django.http import JsonResponse ,HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from userpreferences.models import UserPreferences
import csv



def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__istartswith = search_str, owner = request.user) | Expense.objects.filter(
            date__istartswith = search_str,  owner = request.user) | Expense.objects.filter(
            description__icontains = search_str,  owner = request.user) | Expense.objects.filter(
            category__icontains = search_str,  owner = request.user)

        data = expenses.values()
        return JsonResponse(list(data),safe=False)

# Create your views here.
@login_required(login_url='/authenticate/login')
def index(request):
    categories = Category.objects.all()
    expense = Expense.objects.filter(owner = request.user)
    paginator = Paginator(expense, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)


    try: 
        currency = UserPreferences.objects.get(user = request.user).currency
    except UserPreferences.DoesNotExist:
        currency = None
    context = {
    'expenses' : expense,
    'page_obj':page_obj,
    'currency':currency,
    }
        

    return render(request, 'expenses/index.html',context)

@login_required(login_url='/authenticate/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    if request.method ==  "GET":
        return render(request, 'expenses/add_expense.html', context)

    if request.method ==  "POST":
        context = {
        'categories':categories,
        'values':request.POST
    }
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense-date']


        if not amount:
            messages.error(request, "Amount required")
            return render(request, 'expenses/add_expense.html', context)
        if not description:
            messages.error(request, "Description required")
            return render(request, 'expenses/add_expense.html', context)
        Expense.objects.create(owner = request.user, amount = amount, description = description, category = category, date = date)
        messages.success(request,"Expense saved successfully")
        return redirect('add-expense')


def edit_expense(request,id):
    expense = Expense.objects.get(pk = id)
    context = {
        'expense':expense,
        'values':expense,
        'category_selected' : expense.category,
        'categories' : Category.objects.all()
    }
    if request.method == "GET":
        return render(request, 'expenses/edit_expense.html', context)

    if request.method ==  "POST":
        context = {
        'expense':expense,
        'values':expense,
        'category_selected' : expense.category,
        'categories' : Category.objects.all()
        }

        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['expense-date']


        if not amount:
            messages.error(request, "Amount required")
            return render(request, 'expenses/edit_expense.html', context)
        if not description:
            messages.error(request, "Description required")
            return render(request, 'expenses/edit_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.success(request,"Expense Updated successfully")
        return redirect('expenses')


def delete_expense(request,id):
    expense = Expense.objects.get(pk = id)
    expense.delete()
    messages.info(request, "Expense Deleted")
    return redirect('expenses')


def expense_summary(request):
    return render(request,'expenses/expense_summary.html')



def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename = Expenses_report_' + str(request.user) + '_'+  str(datetime.today().ctime()) + '.csv' 

    writer = csv.writer(response)
    writer.writerow(['Amount', "Description", 'Category', 'Date'])

    expenses = Expense.objects.filter(owner = request.user)
    

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    return response


# Rest Api
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

class ListExpense(APIView):
    # authentication_classes = []
    # permission_classes = []

    def get(self, request, format=None):
        expenses = Expense.objects.filter(owner = request.user)

        lst = {}
        expense_dict ={}
        count = 0 
        for expense in expenses:
            expense_dict['amount']= expense.amount
            expense_dict['description']= expense.description
            expense_dict['category']= expense.category
            expense_dict['date']= expense.date
            lst[count] = expense_dict
            expense_dict ={}
            count+=1

        usernames = [user.username for user in User.objects.all()]
        data = {
            "owner":str(request.user),
            'data':  lst,
            'users':usernames,
        }
        return Response(data)
