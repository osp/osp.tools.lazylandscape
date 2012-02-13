"""
***
"""

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

from sh.models import ShClasses

    
def execPython(cls, request):
    s = '\n'.join([cls.source() ,
                    '__lazylandscape_app = %s_%s()' % (cls.field,cls.name),
                    '__lazylandscape_app.app()',
                    '\n'])
    try:
        sx = compile(s, '<%s.%s>' % (cls.field,cls.name), 'exec')
    except SyntaxError as se:
        r = []
        r.append('<h2>SyntaxError</h2> <a href="#error_%d">%s</a> ' % (se.lineno, str(se)))
        c = 0
        for l in s.splitlines():
            if c == se.lineno:
                r.append('<div id="error_%d"><span style="background-color:red"> %d :</span><code>%s</code> </div>' % (c,c,escape(l)))
            else:
                r.append('<div><span style="background-color:#aaa"> %d :</span><code>%s</code> </div>' % (c,escape(l)))
            c += 1
        return HttpResponse(''.join(r))
        
        
    response = HttpResponse('')
    g = {
        "__builtins__" : __builtins__,
        "request" : request,
        "escape" : escape,
        "response" : response,
        "HttpResponse" : HttpResponse,
        "__name__" : __name__,
        "ShClasses" : ShClasses,
        }
    g['request'] = request
    g['response'] = response
    
    eval(sx, g, {})
    return response
    
@csrf_exempt
def exec_(request, cls):
    try:
        cx = ShClasses.objects.filter(field='Application').filter(name=cls)[0]
    except :
        raise Http404
    
    if cx.public or request.user.is_authenticated():
        if cx.lang == 'python':
            return execPython(cx, request) 
        
        return HttpResponse('<h2>%s not yet supported</h2>' % cx.lang) 
        
    else:
        login_url = '?'.join([reverse('django.contrib.auth.views.login'), '='.join(['next', reverse('sh.app.exec_', args=[cls])])])
        print login_url
        return  HttpResponseRedirect(login_url)
    
    