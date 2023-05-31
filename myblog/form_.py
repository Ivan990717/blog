from django import forms
from myblog.models import UserInfo
from django.forms import widgets #用来渲染{{field字段的样式}}
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError
class UserForm(forms.Form):
    user = forms.CharField(max_length=32,
                           error_messages={"required":"用户名不能为空"},
                           label="用户名",
                           widget=widgets.TextInput(attrs={"class":"form-control"}))
    pwd = forms.CharField(max_length=32,label="密码",
                          error_messages={"required": "密码不能为空"},
                          widget=widgets.TextInput(attrs={"class":"form-control"}))
    re_pwd = forms.CharField(max_length=32,label="密码确认",
                             error_messages={"required": "密码不能为空"},
                             widget=widgets.TextInput(attrs={"class":"form-control"}))
    email = forms.EmailField(max_length=32,label="邮箱",widget=widgets.PasswordInput(attrs={"class":"form-control"}))
# Create your views here.
    def clean_user(self):
        val = self.cleaned_data.get("user")

        user = UserInfo.objects.filter(username=val).first()
        if user:
            raise ValidationError("用户已注册")
        else:
            return val

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        repwd = self.cleaned_data.get("re_pwd")
        if pwd and repwd:
            if pwd == repwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")


