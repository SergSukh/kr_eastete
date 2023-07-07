from django.db.models import Q
from excel_response import ExcelResponse

from .models import Unit
from .views import get_search_max_param, get_search_min_param


def get_header():
    return [[
        'ТИП ОБЪЕКТА',
        'АДРЕС',
        'ПЛОЩАДЬ',
        'ТИП СДЕЛКИ',
        'СТОИМОСТЬ']
    ]


def write_report(units_list):
    data = get_header()
    for unit in units_list:
        data.append([
            unit.name,
            unit.adress(),
            unit.square,
            unit.deal,
            unit.price])
    return data


def get_objs(request):
    deal = request.GET.get('deal')
    name = request.GET.get('q')
    if request.user.is_staff:
        public = None if request.GET.get('public') else True
    else:
        public = True
    sq_min = get_search_min_param(request.GET.get('sq_min'))
    sq_max = get_search_max_param(request.GET.get('sq_max'))
    pr_min = get_search_min_param(request.GET.get('pr_min'))
    pr_max = get_search_max_param(request.GET.get('pr_max'))
    obj_base = Unit.objects.filter(
        Q(deal__iregex=deal),
        Q(name__iregex=name),
        Q(published__answer=public),
        Q(street__street__icontains=request.GET.get('street'))
    )
    objs = []
    for obj in obj_base:
        if (
            obj.check_param(sq_min, obj.square, sq_max)
            and obj.check_param(pr_min, obj.price, pr_max)
        ):
            objs.append(obj)
    return ExcelResponse(write_report(objs))
