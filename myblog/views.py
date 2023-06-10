from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import auth
from myblog.form_ import UserForm
from myblog.models import *


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


from myblog.utils.validCode import get_validCode_img


def get_vaildCode_img(request):
    data = get_validCode_img(request)
    return HttpResponse(data)


def home_site(request,username):
    """
    个人站点生成
    :param request:
    :param username:
    :return:
    """
    user = UserInfo.objects.filter(username = username).first()
    if not user:
        return render(request,"notfound.html")
    # 当前用户对应的所有文章
    blogs = user.blog
    articles = user.article_set.all()

    # 基于__方法: Article.objects.filter(user = user)

    # 查询每一个分类及对应的文章数
        # 每一个表模型object.values().annotate(聚合函数(关联表__统计字段)).values()
    res = Category.objects.values("pk").annotate(c = Count("article__title")).values("title","c")
    print(res) #<QuerySet [{'title': '恩恩爱爱', 'c': 1}]>
    # 查询当前站点的每一个分类及对应的文章数
    cate_list = Category.objects.filter(blog=blogs).values("pk").annotate(c=Count("article__title")).values_list(
        "title", "c")
    print(cate_list) # <QuerySet [('恩恩爱爱', 1)]>
    # 查询当前站点的每一个标签及对应的文章数
    tag_list = Tag.objects.filter(blog=blogs).values("pk").annotate(c=Count("article")).values_list("title","c")
    # 查询当前站点的每一个月的名称及对应的文章数
    ret=Article.objects.extra(select={"is_recent":"create_time > '2022-09-05'"}).values("title","is_recent")
    print(ret) # <QuerySet [{'is_recent': 1, 'title': '这个冬天不太冷'}]>
    """
    日期归档查询
    create table t_mul_new(d date,t time,dt datetime);
    insert into t_mul_new values(now(),now(),now());
    mysql> select date_format(dt,"%Y/%m/%d") from t_mul_new;
        +----------------------------+
        | date_format(dt,"%Y/%m/%d") |
        +----------------------------+
        | 2023/06/09                 |
        +----------------------------+
        1 row in set (0.00 sec)
    
    """
    """
    extra字段：
     xtra(self, select=None, where=None, params=None, tables=None,
              order_by=None, select_params=None):
     有些情况下，Django的语法难以简单的方式表达复杂的where字句，对于这种情况，Django提供了extra()的Queryset机制
     extra可以指定一个或多个参数，必须要有一个
     queryres = Article.objects.extra(select = {"is_recent":"create_time > '2022-09-05'"})
     结果中每个对象都会yo有一个额外的字段is_recent，是一个布尔值，代表是否有该时间段之后的文章
     <QuerySet [<Article: Article object (1)>]>
    """
    # print(Article.objects.extra(select = {"is_recent":"create_time > '2022-09-05'"}).values("title","is_recent"))

    res = Article.objects.extra(select={"y_m_date":"date_format(create_time,'%%Y-%%m-%%d')"}).values("title","y_m_date")
    # < QuerySet[{'y_m_date': '2023-06-04', 'title': '这个冬天不太冷'}] >



    return render(request,"home_site.html")
