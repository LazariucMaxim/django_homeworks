from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    parameter = request.GET.get('sort')
    phones = list(Phone.objects.all())
    if parameter == 'name':
        phones.sort(key=lambda x: x.name)
    elif parameter == 'min_price':
        phones.sort(key=lambda x: x.price)
    elif parameter == 'max_price':
        phones.sort(key=lambda x: x.price, reverse=True)
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]
    context = {'phone': phone}
    return render(request, template, context)
