from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Log, MonthData, create_month_data


# Create your views here.

class Main(APIView):
    def get(self, request):
        log_list = Log.objects.all().order_by('-date')
        month = MonthData.objects.all().order_by('-month')
        create_month_data()

        check, username = checkout(request)
        if not check:
            return render(request, "login.html")

        for log in log_list :
            cargo = log.cargo
            log.cargo = cargo.replace('\r\n','<br/>')
            load = log.load
            log.load = load.replace('\r\n', '<br/>')
            load_pn = log.load_pn
            log.load_pn = load_pn.replace('\r\n', '<br/>')
            qty = log.qty
            log.qty = qty.replace('\r\n', '<br/>')
            gw = log.gw
            log.gw = gw.replace('\r\n', '<br/>')
            cbm = log.cbm
            log.cbm = cbm.replace('\r\n', '<br/>')
            size = log.size
            log.size = size.replace('\r\n', '<br/>')
            unload = log.unload
            log.unload = unload.replace('\r\n', '<br/>')
            pic = log.pic
            log.pic = pic.replace('\r\n', '<br/>')
            load_t = log.load_t
            log.load_t = load_t.replace('\r\n', '<br/>')
            transport = log.transport
            log.transport = transport.replace('\r\n', '<br/>')
            vn = log.vn
            log.vn = vn.replace('\r\n', '<br/>')
            tpn = log.transport_pn
            log.transport_pn = tpn.replace('\r\n','<br/>')

        context = {
            'log_list': log_list,
            'month': month,
            'username': username
        }

        return render(request, "main.html", context=context)


def checkout(request):
    username = request.session.get('username', None)
    check = False
    if username is None:
        return check, username
    from django.contrib.auth.models import User
    user = User.objects.get(username=username)
    if user is None:
        return check, username
    else:
        check = True
        return check, username


def get_logs_by_month(request, year_month):
    # year_month를 '-'를 기준으로 분리
    year, month = year_month.split('-')

    # 선택한 연도와 월에 해당하는 로그 데이터를 가져오기
    logs = Log.objects.filter(date__year=year, date__month=month).order_by('-date')
    months = MonthData.objects.all().order_by('-month')

    for log in logs:
        cargo = log.cargo
        log.cargo = cargo.replace('\r\n', '<br/>')
        load = log.load
        log.load = load.replace('\r\n', '<br/>')
        load_pn = log.load_pn
        log.load_pn = load_pn.replace('\r\n', '<br/>')
        qty = log.qty
        log.qty = qty.replace('\r\n', '<br/>')
        gw = log.gw
        log.gw = gw.replace('\r\n', '<br/>')
        cbm = log.cbm
        log.cbm = cbm.replace('\r\n', '<br/>')
        size = log.size
        log.size = size.replace('\r\n', '<br/>')
        unload = log.unload
        log.unload = unload.replace('\r\n', '<br/>')
        pic = log.pic
        log.pic = pic.replace('\r\n', '<br/>')
        load_t = log.load_t
        log.load_t = load_t.replace('\r\n', '<br/>')
        transport = log.transport
        log.transport = transport.replace('\r\n', '<br/>')
        vn = log.vn
        log.vn = vn.replace('\r\n', '<br/>')
        tpn = log.transport_pn
        log.transport_pn = tpn.replace('\r\n', '<br/>')

    # 로그 데이터를 JSON 형태로 반환
    context = {
        'log_list': logs,
        'month': months,
        'year_month': year_month,
    }
    return render(request, "check.html", context=context)


class UploadLog(APIView):
    def post(self, request):
        pk = request.data.get('pk')
        date = request.data.get('date')
        cargo = request.data.get('cargo')
        load = request.data.get('load')
        load_pn = request.data.get('load_pn')
        qty = request.data.get('qty')
        gw = request.data.get('gw')
        cbm = request.data.get('cbm')
        size = request.data.get('size')
        unload = request.data.get('unload')
        pic = request.data.get('pic')
        load_t = request.data.get('load_t')
        transport = request.data.get('transport')
        vn = request.data.get('vn')
        transport_pn = request.data.get('transport_pn')
        print(pk)
        log_instence, created = Log.objects.update_or_create(pk=pk, defaults={'date': date, 'cargo': cargo,
                                                                              'load': load, 'load_pn': load_pn,
                                                                              'qty': qty,
                                                                              'gw': gw, 'cbm': cbm, 'size': size,
                                                                              'unload': unload, 'pic': pic,
                                                                              'load_t': load_t, 'transport': transport,
                                                                              'vn': vn, 'transport_pn': transport_pn}, )
        if created:
            return Response(status=200, data=dict(message='생성완료'))
        else:
            return Response(status=203)


class DeleteLogView(APIView):
    def post(self, request, log_id):
        checkout(request)
        try:
            log = Log.objects.get(pk=log_id)
            log.delete()
            return Response(status=200)
        except Log.DoesNotExist:
            return Response(status=403)


class Get_log(APIView):
    def get(self, request):
        try:
            log_id = request.GET.get('log_id', None)
            log = Log.objects.get(pk=log_id)
            if log is None:
                Response(status=203)

            data = {
                'log': {
                    'id': log.id,
                    'date': log.date,
                    'cargo': log.cargo,
                    'load': log.load,
                    'load_pn': log.load_pn,
                    'qty': log.qty,
                    'gw': log.gw,
                    'cbm': log.cbm,
                    'size': log.size,
                    'unload': log.unload,
                    'pic': log.pic,
                    'load_t': log.load_t,
                    'transport': log.transport,
                    'vn': log.vn,
                    'transport_pn': log.transport_pn
                }
            }
            return Response(status=202, data=data)
        except Log.DoesNotExist:
            return Response(status=403)
