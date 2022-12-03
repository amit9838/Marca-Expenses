from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from .models import UserIncome, Source
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
import json
from django.http import JsonResponse



def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expense = UserIncome.objects.filter(
            amount__istartswith = search_str, owner = request.user) | UserIncome.objects.filter(
            date__istartswith = search_str,  owner = request.user) | UserIncome.objects.filter(
            description__icontains = search_str,  owner = request.user) | UserIncome.objects.filter(
            source__icontains = search_str,  owner = request.user)

        data = expense.values()
        return JsonResponse(list(data),safe=False)


# Create your views here.
@login_required(login_url='/authenticate/login')
def index(request):

    income = UserIncome.objects.filter(owner = request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)



    currency = UserPreferences.objects.get(user = request.user).currency
    context = {
    'income' : income,
    'page_obj':page_obj,
    'currency':currency,
    }
        

    return render(request, 'income/index.html',context)

@login_required(login_url='/authenticate/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources':sources,
    }
    if request.method ==  "GET":
        return render(request, 'income/add_income.html', context)

    if request.method ==  "POST":
        context = {
        'sources':sources,
        'values':request.POST
    }
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income-date']


        if not amount:
            messages.error(request, "Amount required")
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, "Description required")
            return render(request, 'income/add_income.html', context)
        UserIncome.objects.create(owner = request.user, amount = amount, description = description, source = source, date = date)
        messages.success(request,"Record saved successfully")
        return redirect('add-income')




def edit_income(request,id):
    income = UserIncome.objects.get(pk = id)
    context = {
        'income':income,
        'values':income,
        'source_selected' : income.source,
        'sources' : Source.objects.all()
    }
    if request.method == "GET":
        return render(request, 'income/edit_income.html', context)

    if request.method ==  "POST":
        context = {
        'income':income,
        'values':income,
        'source_selected' : income.source,
        'sources' : source.objects.all()
        }

        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['income-date']


        if not amount:
            messages.error(request, "Amount required")
            return render(request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, "Description required")
            return render(request, 'income/edit_income.html', context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.source = source
        income.date = date
        income.save()
        messages.success(request,"income Updated successfully")
        return redirect('income')



def delete_income(request,id):
    income = UserIncome.objects.get(pk = id)
    income.delete()
    messages.info(request, "Income Deleted")
    return redirect('income')