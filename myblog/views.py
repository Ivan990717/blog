from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from myblog.form_ import UserForm
from myblog.models import *
from myblog.utils.validCode import get_validCode_img
from django.db.models.functions import TruncMonth  # 截断到月份
# 先导系统模块，然后导入第三方插件，之后导入自定义模块
def index(request):
    article_list = Article.objects.all()

    return render(request, "index.html",{"article_list":article_list})

def log_out(request):
    auth.logout(request) # 等同于request.session.flush() 删掉了存储信息
    return redirect("/login/")


def register(request):
    res = {"user": None, "msg": None}
    if request.is_ajax():
        form = UserForm(request.POST)
        if form.is_valid():
            # 生成用户数据
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            ava = request.FILES.get("avatar")
            res["user"] = form.cleaned_data.get("user")
            extra_field = {}
            if ava:
                extra_field["avatar"] = ava

            UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra_field)
            # avatar = ava :上传了一个对象，然后下载到了项目的根目录，avatar存的是文件的路径


        else:
            res["msg"] = form.errors
        return JsonResponse(res)
    f = UserForm()
    return render(request, "register.html", {"form": f})


def login(request):
    if request.method == "POST":  # 不能写成post
        res = {
            "user": None,
            "msg": None
        }
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_str = request.POST.get("code_img")
        valid_code = request.session.get("valid_code")

        if valid_str.upper() == valid_code.upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)
                res['user'] = user.username
            else:
                res['msg'] = "username or password error"
        else:
            res["msg"] = "valid code error"

        return JsonResponse(res)

        # 验证码比对时需要get_vaildCode_img函数内的值，但是
        # 用global定义验证码会导致多个验证码的混乱，所以在get_vaildCode_img
        # 内直接把验证码存到session当中，然后在这个视图函数内取出来比较

    return render(request, "login.html")





def get_vaildCode_img(request):
    data = get_validCode_img(request)
    return HttpResponse(data)


def home_site(request,username, **kwargs):
    """
    个人站点生成
    :param request:
    :param username:
    :param kwargs: 如果有值，可以跳转到分类下面
    :return:
    """

    user = UserInfo.objects.filter(username = username).first()
    if not user:
        return render(request,"notfound.html")
    # 当前用户对应的所有文章
    article_list = Article.objects.filter(user=user)
    if kwargs:
        print(kwargs)
        condition = kwargs.get("condition")
        params = kwargs.get("param")
        if condition == "category":
            articles = Article.objects.filter(user = user).filter(category__title=params)
        elif condition == "tag":
            articles = Article.objects.filter(user = user).filter(tags__title=params)
        elif condition == "archive":
            year,month = params.split("-")
            articles = Article.objects.filter(user = user).filter(create_time__month=month,create_time__year=year)

    blog = user.blog
    # content = getClassificationData(username)



    return render(request,"home_site.html", {"username":username,"blog":blog,"article_list":article_list})



def article_detail(request,username,article_id):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article_obj = Article.objects.filter(pk = article_id).first()
    # print(blogs.title)
    # content = getClassificationData(username)
    # return render(request,"article_detail.html",locals())
    # 在Django的视图函数中，locals()函数被用来将当前作用域的局部变量以字典形式传递给模板。它是Python内置函数，返回的是包含当前作用域所有局部变量的字典。
    return render(request, "article_detail.html",{"username":username,"blog":blog, "article_obj":article_obj})
