# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, redirect
from forms import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from web.models import Book, Reader, Circulation
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.http import HttpResponse

def index(request):
    return render_to_response('index.html', context_instance=RequestContext(request))

# 使用者登入功能
def user_login(request):
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # 登入成功，導到大廳
                login(request, user)
                return redirect('/')
            else:
                message = "無效的帳號或密碼!"
    else:
        form = LoginForm()
    return render_to_response('login.html', {'message': message, 'form': form}, context_instance=RequestContext(request))

def book(request):
  keyword = request.GET.get('book')
  if keyword != None:
    books = Book.objects.filter(title__icontains=keyword).order_by('-id')
  else:
    books = Book.objects.all().order_by('-id')
  return render_to_response('book.html', {'books': books, 'keyword': keyword}, context_instance=RequestContext(request))

def book_add(request):
  if request.method == "POST":
    form = BookForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/book')
  else:
    form = BookForm()
  return render_to_response('form.html', {'form': form}, context_instance=RequestContext(request))

def book_delete(request, book_id):
  try:
    book = Book.objects.get(id=book_id).delete()
  except ObjectDoesNotExist:
    pass
  return redirect('/book')

def reader(request):
  keyword = request.GET.get('reader')
  if keyword != None:
    readers = Reader.objects.filter(realname__contains=keyword).order_by('-id')
  else:
    readers = Reader.objects.all().order_by('-id')
  return render_to_response('reader.html', {'readers': readers, 'keyword': keyword}, context_instance=RequestContext(request))

def reader_add(request):
  if request.method == 'POST':
    form = ReaderForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('/reader')
  else:
    form = ReaderForm()
  return render_to_response('form.html', {'form': form}, context_instance=RequestContext(request))

def reader_delete(request, reader_id):
  try:
    reader = Reader.objects.get(id=reader_id).delete()
  except ObjectDoesNotExist:
    pass
  return redirect('/reader')

def reader_view(request, reader_id):
  reader = Reader.objects.get(id=reader_id)
  if request.method == 'POST':
    form = ReaderForm(request.POST, instance=reader)
    if form.is_valid():
      form.save()
  else:
    form = ReaderForm(instance=reader)
  circulations = Circulation.objects.filter(reader=reader).order_by('-id')
  return render_to_response('reader_view.html', {'reader': reader, 'circulations': circulations, 'form': form}, context_instance=RequestContext(request))

def book_view(request, book_id):
  book = Book.objects.get(id=book_id)
  if request.method == 'POST':
    form = BookForm(request.POST, instance=book)
    if form.is_valid():
      form.save()
  else:
    form = BookForm(instance=book)
  circulations = Circulation.objects.filter(book=book).order_by('-id')
  return render_to_response('book_view.html', {'book': book, 'circulations': circulations, 'form': form}, context_instance=RequestContext(request))

def book_checkout(request, reader_id=None, book_id=None):
  if not reader_id:
    keyword = request.POST.get('keyword')
    if keyword != None:
      readers = Reader.objects.filter(realname__contains=keyword).order_by('-id')
    else:
      readers = Reader.objects.all().order_by('-id')
    return render_to_response('circulation_reader.html', {'readers': readers, 'keyword': keyword, 'operation': '借書'}, context_instance=RequestContext(request))

  try:
    reader = Reader.objects.get(id=int(reader_id))
  except ObjectDoesNotExist:
    return redirect('/book/checkout')

  off_shelf_book_ids = [circulation.book.id for circulation in Circulation.objects.filter(date_return=None)]
  
  if book_id:
    try:
      book = Book.objects.get(id=int(book_id))
      if not book_id in off_shelf_book_ids:
        circulation = Circulation(reader=reader, book=book, date_checkout=datetime.now())
        circulation.save()
    except ObjectDoesNotExist:
      pass
    return redirect('/book/checkout/'+str(reader_id))
  
  borrowing = Circulation.objects.filter(reader=reader, date_return=None)
  keyword = request.POST.get('keyword')
  if keyword != None:
    books = Book.objects.filter(title__icontains=keyword).exclude(id__in=off_shelf_book_ids).order_by('-id')
  else:
    books = Book.objects.exclude(id__in=off_shelf_book_ids).order_by('-id')
  
  return render_to_response('circulation_book.html', {'reader': reader, 'borrowing': borrowing, 'books': books, 'keyword': keyword, 'operation': '借書'}, context_instance=RequestContext(request))

def book_return(request, book_id=None):
  if book_id:
    try:
      book = Book.objects.get(id=book_id)
      circulation = Circulation.objects.get(book=book, date_return=None)
      circulation.date_return = datetime.now()
      circulation.save()
    except ObjectDoesNotExist:
      pass
    
    return redirect('/book/return/')
  
  if request.method == 'POST':
    form = CirculationForm(request.POST)
  else:
    form = CirculationForm()

  off_shelf_book_ids = [circulation.book.id for circulation in Circulation.objects.filter(date_return=None)]
  keyword = request.POST.get('keyword')
  if keyword != None:
    books = Book.objects.filter(title__icontains=keyword, id__in=off_shelf_book_ids).order_by('-id')
  else:
    books = Book.objects.filter(id__in=off_shelf_book_ids).order_by('-id')

  return render_to_response('circulation_book.html', {'form': form, 'books': books, 'keyword': keyword, 'operation': '還書'}, context_instance=RequestContext(request))

def circulation(request):
  return render_to_response('circulation.html', context_instance=RequestContext(request))

def circulation_combo(request):
  message = ''
  reader = None
  circulations = None
  if request.method == 'POST':
    form = CirculationForm(request.POST)
    if form.is_valid():
      entityid = form.cleaned_data['entityid']
      rid = form.cleaned_data['rid']
      try:
        if entityid[0] == 'R':
          reader = Reader.objects.get(id=int(entityid[1:]))        
          form = CirculationForm(initial={'entityid':entityid, 'rid':reader.id})
          message = '切換讀者'
        elif entityid[0] == 'B':
          book = Book.objects.get(id=int(entityid[1:]))
          circulations = Circulation.objects.filter(book=book, date_return=None)
          
          if circulations:
            reader = circulations[0].reader
            if (not rid or int(rid) == reader.id):
              message = '還書'
              circulation = circulations[0]
              circulation.date_return = datetime.now()
              circulation.save()
            else:
              message = '錯誤！該書籍出借中，無法借書！'
              reader = Reader.objects.get(id=int(rid))
          elif rid:
              message = '借書'
              reader = Reader.objects.get(id=int(rid))
              circulation = Circulation(reader=reader, book=book, date_checkout=datetime.now())
              circulation.save()
              reader = circulation.reader
          else:
            message = '錯誤！該書籍未出借，無法還書！'
      except ObjectDoesNotExist:
        message = '無此讀者或書籍'
        form = CirculationForm()

      if reader:
        circulations = Circulation.objects.filter(reader=reader).order_by('-id')
  else:
    form = CirculationForm();
  form['entityid'].label = '請輸入讀者編號或書籍編號'
  return render_to_response('circulation_combo.html', {'form': form, 'message': message, 'reader': reader, 'circulations': circulations}, context_instance=RequestContext(request))