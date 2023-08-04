from django import template
from django.db.models.functions import TruncMonth

from myblog.models import *
from django.db.models import Count
"""
Django中的templatetags是一个非常有用的功能，它允许你在模板中创建自定义的标记和过滤器。换句话说，templatetags可以让你扩展Django模板引擎的能力。

有两种类型的模板标签：

简单标签：这些标签处理任何参数，并返回一个字符串结果。此结果将被直接插入到模板的输出中。
包含标签：这些标签处理参数并返回一个渲染的模板。
下面是一些使用场景：

计算一些值并将其插入到模板中。例如，你可能希望在模板中显示当前时间，或者基于某些复杂逻辑显示特定文本。
为模板提供额外的通用函数。例如，你可能想要创建一个以特殊方式格式化日期的标签。
包含其他模板并传入一些变量。例如，你可能有一个显示用户信息的小部件，并且希望在多个地方重复使用它。
下面是如何创建一个简单的templatetag：

在你的Django应用文件夹下创建一个名为templatetags的目录。
在该目录下，创建一个python文件，例如my_tags.py。
在这个python文件中，你可以定义你自己的标签或过滤器。
"""
register = template.Library()

"""
注意，在使用自定义模板标签之前，必须先使用{% load %}标签加载它们。

简而言之，templatetags在Django中非常有用，它们让你可以编写更加复杂、更具交互性的模板。
"""
@register.simple_tag
def multi_tag(x,y):
    return x*y

# 必须重启app
@register.inclusion_tag("classification.html") # 括号中引入模板语法
def get_classification_style(username):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    # 基于__方法: Article.objects.filter(user = user)

    # 查询每一个分类及对应的文章数
    # 每一个表模型object.values().annotate(聚合函数(关联表__统计字段)).values()
    res = Category.objects.values("pk").annotate(c=Count("article__title")).values("title", "c")
    print(res)  # <QuerySet [{'title': '恩恩爱爱', 'c': 1}]>
    # 查询当前站点的每一个分类及对应的文章数
    cate_list = Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list(
        "title", "c")
    # print(cate_list)  # <QuerySet [('恩恩爱爱', 1)]>
    # 查询当前站点的每一个标签及对应的文章数
    tag_list = Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title", "c")
    # 查询当前站点的每一个月的名称及对应的文章数
    ret = Article.objects.extra(select={"is_recent": "create_time > '2022-09-05'"}).values_list("title", "is_recent")
    # print(ret)  # <QuerySet [{'is_recent': 1, 'title': '这个冬天不太冷'}]>

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

    # date_list = Article.objects.filter(user=user).extra(select={"y_m_date":"date_format(create_time,'%%Y-%%m-%%d')"}).values("y_m_date").annotate(c = Count("nid")).values_list("y_m_date","c")
    date_list = Article.objects.filter(user=user).extra(
        select={"y_m_date": "date_format(create_time,'%%Y-%%m')"}).values("y_m_date").annotate(
        c=Count("nid")).values_list("y_m_date", "c")
    """
    时间归档格式要注意一下
    """
    # <QuerySet [{'y_m_date': '2023-06-04', 'c': 1}, {'y_m_date': '2023-06-10', 'c': 1}]>

    """
    django中的日期归档查询
    """

    date = Article.objects.filter(user=user).annotate(month=TruncMonth("create_time")).values("month").annotate(
        c=Count("nid")).values_list("month", "c")
    # <QuerySet [(datetime.datetime(2023, 6, 1, 0, 0), 2)]>

    return {"blog": blog, "cate_list": cate_list, "date_list": date_list, "tag_list": tag_list}