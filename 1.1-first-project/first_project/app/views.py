from django.http import HttpResponse
from django.shortcuts import render, reverse
import datetime
import os
import pprint


def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.datetime.now().time()
    msg = f'<h1>Текущее время: {current_time}</h1>'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    workdir = {'first_project': os.listdir()}
    workdir['first_project'].remove('venv')
    workdir['first_project'] = list(map(lambda x: {x: os.listdir(x)} if '.' not in x else x, workdir['first_project']))
    print(pprint.pformat(workdir))
    return HttpResponse(f'<h1><pre>{pprint.pformat(workdir)}</pre></h1>')
    raise NotImplemented
