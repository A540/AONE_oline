from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class Login(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # print(request)
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        # print(username, password)
        if username is None:
            return Response(status=500, data=dict(message='이메일을 입력해주세요'))

        if password is None:
            return Response(status=500, data=dict(message='비밀번호를 입력해주세요'))

        user = User.objects.get(username=username)

        if user is None:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        from django.contrib.auth.hashers import check_password
        if check_password(password, user.password) is False:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        request.session['loginCheck'] = True
        request.session['username'] = user.username

        return Response(status=200, data=dict(message='로그인에 성공했습니다.'))

class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "login.html")