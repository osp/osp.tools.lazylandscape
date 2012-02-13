from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(request.POST['redirect'])
   

                

def view(request):
    if request.POST['login']:
        return log_in(request)
    else:
        render_to_response("login.html", {'redirect':request.path}, context_instance = RequestContext(request))