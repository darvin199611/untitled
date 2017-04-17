from django.shortcuts import render
from django.utils import timezone
from Store.models import Market, Sale, Stuff
from Store.help_functions import check_premissions


def control(request):
    market_choose = False
    markets = Market.list(request)
    return render(request, 'Control/control.html', {'markets': markets, 'market_choose': market_choose})


def store_control(request, id):
    market_id = id
    market = Market.objects.get(id=id)
    check_premissions(request, market)  # функция проверяет принадлежит ли запрашиваемый экземпляр пользователю ,
    # если нет , возвращает 404
    sales = Sale.objects.filter(stuff__market_id=market_id)
    print(sales)
    stuffs = Stuff.objects.filter(market_id=market_id).order_by('created')
    stuff = []
    sale = []
    for obj in sales:
        sale_list = {'stuff_name': obj.stuff,
                     'date': (timezone.localtime(obj.created)).strftime('%Y-%m-%d %H:%M')}
        sale.append(sale_list)
    for obj in stuffs:
        stuffss = {'id': obj.id, 'name': obj.name, 'picture': obj.picture,
                   'price': str(obj.price), 'amount': str(obj.amount),
                   'date': (timezone.localtime(obj.created)).strftime('%Y-%m-%d %H:%M')}
        stuff.append(stuffss)
    market_choose = True
    return render(request, 'Control/control.html', {'market_choose': market_choose, 'stuffs': stuff, 'sales': sale, })
