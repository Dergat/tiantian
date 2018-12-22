from django.http import HttpResponseRedirect
#如果未登陆就跳转到登陆页面

def login(func):
    def login_fun(reuest,*args,**kwargs):
        if reuest.session.has_key('user_id'):
            return func(reuest,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.get_full_path())
            return red

    return login_fun