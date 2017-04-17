from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from Store.models import Market, Stuff, Sale
from django.http import HttpResponse
from datetime import datetime as dt, timedelta
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
    return render(request, 'Control/control.html', {'market_choose': market_choose, 'stuffs': stuff, 'sales': sale,
                                                    'market_created': market.created})


def take_sales(request):
    date_start = request.GET['date_start']
    date_end = request.GET['date_end']
    date_end = dt.strptime(date_end, "%d.%m.%Y")
    date_start = dt.strptime(date_start, "%d.%m.%Y")
    date_end = date_end + timedelta(days=1)  # добавляем к date_end 1 день, чтоб выводило данные за выбраный
    #  диапазон
    # включительно 0
    data = Sale.objects.filter(created__range=[date_start, date_end]).filter(active=True)
    sales_json = []
    for si in data:
        sales_json.append({'stuff': si.stuff.name, 'price': str(si.stuff.price),
                           'dt': (timezone.localtime(si.created)).strftime('%Y-%m-%d %H:%M'), 'id': si.id})
    response_data = {
        'sales': sales_json
    }

    return JsonResponse(response_data)


def delete_sale(request):
    if request.POST:
        sale_id = request.POST['sale_id']
        sale = Sale.objects.get(id=sale_id)
        sale.active = False
        sale.save()
        return HttpResponse("yes", content_type='text/html')
    else:
        return HttpResponse("Error", content_type='text/html')