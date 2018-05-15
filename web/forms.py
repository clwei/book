# -*- coding: UTF-8 -*-
from django import forms
from web.models import Book, Reader

# 使用者登入表單
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)        
        self.fields['username'].label = "帳號"
        self.fields['password'].label = "密碼"

# 書籍資料表單
class BookForm(forms.ModelForm):
  class Meta:
    model = Book
    fields = ['title', 'author']
    labels = {
      'title': '書名', 
      'author': '作者',
    }

# 讀者資料表單
class ReaderForm(forms.ModelForm):
  class Meta:
    model = Reader
    fields = '__all__'
    labels = {
      'realname': '姓名', 
      'phone': '連絡電話',
    }

# 流通紀錄表單
class CirculationForm(forms.Form):
  # 書籍或讀者編號
  entityid = forms.RegexField(regex='(R|B)(\d{6})', error_messages={'required': '請輸入讀者編號或書籍編號', 'invalid': '不合法的讀者或書籍編號'})
  # 目前作用中的讀者
  rid = forms.RegexField(regex='\d*', required=False, widget=forms.HiddenInput())
