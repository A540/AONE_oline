from django.db import models


# Create your models here.
class Log(models.Model):
    date = models.DateField(auto_now=False)  # 년 월 일 (요일)
    cargo = models.TextField()  # 화주
    load = models.TextField()  # 상차지
    load_pn = models.TextField()  # 전화번호(상차지)
    qty = models.TextField()  # 수량
    gw = models.TextField()  # 중량
    cbm = models.TextField()  # 용적
    size = models.TextField()  # 사이즈
    unload = models.TextField()  # 하차지
    pic = models.TextField()  # 담당자
    load_t = models.TextField()  # 시간(상차시간)
    transport = models.TextField()  # 운송사
    vn = models.TextField()  # 차번
    transport_pn = models.TextField()  # 연락처(기사)


class MonthData(models.Model):
    month = models.TextField(max_length=10)  # 월 데이터를 저장할 필드


# 새로운 모델에 데이터 저장하는 함수
def create_month_data():
    # 원본 모델의 모든 객체 가져오기
    logs = Log.objects.all()

    for log in logs:
        # 원본 모델의 date 필드에서 월 데이터 추출
        month_data = log.date.strftime('%Y-%m')  # YYYY-MM 형식의 문자열로 변환

        # 이미 존재하는지 확인
        existing_month_data = MonthData.objects.filter(month=month_data).first()

        if existing_month_data:
            # 이미 존재하는 경우, 해당 객체의 로그를 업데이트하고 중복 데이터 삭제
            existing_month_data.log = log
            existing_month_data.save()
        else:
            # 존재하지 않는 경우 새로운 객체 생성
            MonthData.objects.create(month=month_data)
