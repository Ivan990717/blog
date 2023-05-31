from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib import auth
from myblog.form_ import UserForm
from myblog.models import UserInfo
def index(request):
    return render(request,"index.html")

def register(request):
    res = {"user":None,"msg":None}
    if request.is_ajax():
        form = UserForm(request.POST)
        if form.is_valid():
            #生成用户数据
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            ava = request.FILES.get("avatar")
            res["user"] = form.cleaned_data.get("user")
            user_obj = UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=ava)
            # avatar = ava :上传了一个对象，然后下载到了项目的根目录，avatar存的是文件的路径


        else:
            res["msg"] = form.errors
        return JsonResponse(res)
    f = UserForm()
    return render(request,"register.html",{"form":f})

def login(request):
    if request.method=="POST": #不能写成post
        res = {
            "user":None,
            "msg":None
        }
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_str = request.POST.get("code_img")
        valid_code = request.session.get("valid_code")

        if valid_str.upper() == valid_code.upper():
            user = auth.authenticate(username=user,password = pwd)
            if user:
                auth.login(request,user)
                res['user'] = user.username
            else:
                res['msg'] = "username or password error"
        else:
            res["msg"] = "valid code error"

        return JsonResponse(res)


        # 验证码比对时需要get_vaildCode_img函数内的值，但是
        # 用global定义验证码会导致多个验证码的混乱，所以在get_vaildCode_img
        # 内直接把验证码存到session当中，然后在这个视图函数内取出来比较



    return render(request,"login.html")
from myblog.utils.validCode import get_validCode_img
def get_vaildCode_img(request):
    data = get_validCode_img(request)
    return HttpResponse(data)