#encoding:utf8
from django.shortcuts import render,redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from df_goods.models import GoodsInfo

# Create your views here.
def register(request):
    return  render(request,'df_user/register.html')

def register_handle(request):
    #接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')



#加密
    s1 = sha1()
    s1.update(upwd.encode("utf-8")) #必须指定要加密的字符串的字符编码
    upwd3=s1.hexdigest()   #获取加密结果

 #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
#注册成功，转到登录页面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)

    users = UserInfo.objects.filter(uname=uname)


    if len(users) == 1:
        s1=sha1()
        s1.update(upwd.encode("utf-8"))
        if s1.hexdigest()==users[0].upwd:
            red = HttpResponseRedirect('/user/info/')

            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            return red
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)


def logout(request):
    del request.session['user_id']
    del request.session['user_name']
    return redirect('/')

def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail


    goods_ids1=request.session.get(str(request.session['user_id']),'')
    goods_list=[]
    for goods_id in goods_ids1:
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {'title':'用户中心',
               'user_name':request.session['user_name'],
               'user_email': user_email,
               'goods_list': goods_list,
            }
    return render(request,'df_user/user_center_info.html',context)



def order(request):
    context = {'title':'用户中心'}
    return render(request,'df_user/user_center_order.html',context)

'''
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        if not(user.ushou and user.uaddress and user.uyoubian and user.uphone):
            return redirect('/user/site')
        context = {'title':'用户中心','user':user}
        user.save()
        return render(request,'df_user/user_center_site.html',context)
'''
def site(request):      #收货地址
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        if not(user.ushou and user.uaddress and user.uaddress and user.uphone):
            return redirect('/user/site/')
    context = {'title': '用户中心', 'user': user}
    user.save()
    return render(request, 'df_user/user_center_site.html', context)
