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

        username = request.session.get('username', None)
        if username is None:
            return render(request, "login.html")
        from django.contrib.auth.models import User
        user = User.objects.get(username=username)
        if user is None:
            return render(request, "login.html")

        context = {
            'log_list': log_list,
            'month': month,
            'username': username
        }

        return render(request, "main.html", context=context)


def get_logs_by_month(request, year_month):
    # year_month를 '-'를 기준으로 분리
    year, month = year_month.split('-')
    print(year, month)

    # 선택한 연도와 월에 해당하는 로그 데이터를 가져오기
    logs = Log.objects.filter(date__year=year, date__month=month)
    month = MonthData.objects.all().order_by('-month')

    # 로그 데이터를 JSON 형태로 반환
    context = {
        'log_list': logs,
        'month': month
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

        Log.objects.create(pk=pk, date=date, cargo=cargo, load=load, load_pn=load_pn, qty=qty, gw=gw, cbm=cbm,
                           size=size, unload=unload, pic=pic, load_t=load_t, transport=transport,
                           vn=vn, transport_pn=transport_pn)

        return Response(status=200)


class DeleteLogView(APIView):
    def post(self, request, log_id):
        try:
            log = Log.objects.get(pk=log_id)
            log.delete()
            return Response(status=200)
        except Log.DoesNotExist:
            return Response(status=404)
