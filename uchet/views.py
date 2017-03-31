import pickle

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.core import serializers
from django.utils import timezone
from django.utils.datetime_safe import datetime

from uchet.models import UserProfile, Market, Stuff, Sale
from .forms import UserForm, UserProfileForm


def main(request):
    if request.user.is_authenticated:
        markets = Market.spisok(request)
        return render(request, 'uchet/main.html', {'markets': markets})
    else:
        return render(request, 'uchet/main.html')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Теперь мы хэшируем пароль с помощью метода set_password.
            # После хэширования мы можем обновить объект "пользователь".
            user.set_password(user.password)
            user.save()

            # Теперь разберемся с экземпляром UserProfile.
            # Поскольку мы должны сами назначить атрибут пользователя, необходимо приравнять commit=False.
            # Это отложит сохранение модели, чтобы избежать проблем целостности.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Предоставил ли пользователь изображение для профиля?
            # Если да, необходимо извлечь его из формы и поместить в модель UserProfile.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Теперь мы сохраним экземпляр модели UserProfile.
            profile.save()

            # Обновляем нашу переменную, чтобы указать, что регистрация прошла успешно.
            registered = True

        # Неправильная формы или формы - ошибки или ещё какая-нибудь проблема?
        # Вывести проблемы в терминал.
        # Они будут также показаны пользователю.
        else:
            print(user_form.errors, profile_form.errors)

    # Не HTTP POST запрос, следователь мы выводим нашу форму, используя два экземпляра ModelForm.
    # Эти формы будут не заполненными и готовы к вводу данных от пользователя.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Выводим шаблон в зависимости от контекста.
    return render(request,
                  'uchet/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # Если запрос HTTP POST, пытаемся извлечь нужную информацию.
    if request.method == 'POST':
        # Получаем имя пользователя и пароль, вводимые пользователем.
        # Эта информация извлекается из формы входа в систему.
        # Мы используем request.POST.get('<имя переменной>') вместо request.POST['<имя переменной>'],
        # потому что request.POST.get('<имя переменной>') вернет None, если значения не существует,
        # тогда как request.POST['<variable>'] создаст исключение, связанное с отсутствем значения с таким ключом
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Используйте Django, чтобы проверить является ли правильным
        # сочетание имя пользователя/пароль - если да, то возвращается объект User.
        user = authenticate(username=username, password=password)

        # Если мы получили объект User, то данные верны.
        # Если получено None (так Python представляет отсутствие значения), то пользователь
        # с такими учетными данными не был найден.
        if user:
            # Аккаунт активен? Он может быть отключен.
            if user.is_active:
                # Если учетные данные верны и аккаунт активен, мы можем позволить пользователю войти в систему.
                # Мы возвращаем его обратно на главную страницу.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # Использовался не активный аккуант - запретить вход!
                return HttpResponse("Your account is disabled.")
        else:
            # Были введены неверные данные для входа. Из-за этого вход в систему не возможен.
            print("Invalid login details: {0}, {1}".format(username, password))
            if username or password == 0:
                error = "Неверный логин или пароль"
            else:
                error = "заполните все поля"
            return render(request, 'uchet/login.html', {'error': error})

    # Запрос не HTTP POST, поэтому выводим форму для входа в систему.
    # В этом случае скорее всего использовался HTTP GET запрос.
    else:
        # Ни одна переменная контекста не передается в систему шаблонов, следовательно, используется
        # объект пустого словаря...
        return render(request, 'uchet/login.html', {})


@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'uchet/profile.html', {'profile': profile, 'user': user})


@login_required
def profile__edit(request):
    profile = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(request.POST, request.FILES or None, instance=profile, auto_id=False)

    if request.POST:
        if form.is_valid():
            form.save()
        return redirect('profile__edit')
    else:
        usrform = UserProfileForm(instance=profile)

    return render(request, 'uchet/profile__edit.html', {'form': usrform, 'profile': profile}, )


def market_detail(request, id):
    market = get_object_or_404(Market, id=id)
    stuffs = Stuff.objects.filter(market_id=id).order_by('created_date')

    return render(request, 'uchet/market_detail.html', {'market': market, 'stuffs': stuffs})


def get_market_sales(request):
    if request.GET:
        market_id = request.GET['market_id']
        today = datetime.now()
        data = Sale.objects.filter(stuff__market_id=market_id)
        data = data.filter(datetime__day=today.day, datetime__month=today.month, datetime__year=today.year)
        submissions_json = []
        for si in data:
            submissions_json.append({'stuff': si.stuff.name, 'price': str(si.stuff.price),
                                     'dt': (timezone.localtime(si.datetime)).strftime('%Y-%m-%d %H:%M')})
        response_data = {
            'submissions': submissions_json
        }

        return HttpResponse(json.dumps(response_data),
                            content_type="application/json")


def check_login(request):
    if request.GET:
        data = User.objects.filter(username=request.GET['username']).exists()
        if data:
            return HttpResponse("no", content_type='text/html')
        else:
            return HttpResponse("yes", content_type='text/html')


def get_stuff(request):
    if request.method == 'POST':
        stuff_pk = request.POST.get('stuff_pk')
        market_id = request.POST.get('market_id')
        st = Stuff.objects.filter(market_id=market_id)
        stuffget = st.get(id=stuff_pk)
        stuffs = {'name': stuffget.name, 'description': stuffget.description, 'picture': str(stuffget.picture),
                  'price': str(stuffget.price), 'amount': str(stuffget.amount)}

        response_data = {
            'stuffs': stuffs
        }

        return JsonResponse(response_data)

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def make_sale(request):
    if request.method == "POST":
        stuff_pk = request.POST.get('stuff_pk')
        sale = Sale(stuff_id=stuff_pk)
        sale.save()
        return HttpResponse("done")
