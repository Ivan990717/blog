from django.contrib import admin
# 进行admin注册
# 将生成的数据库导入admin管理系统，这样访问index页面就可以直接从这里面导入数据
from myblog.models import *

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(Article2Tag)
admin.site.register(ArticleUpDown)
# Register your models here.
