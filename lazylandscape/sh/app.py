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

tab = '    '
    

def execPython(cls, request):
    app = '\n'.join(['lazylandscape_app = %s.%s()' % (cls.field,cls.name),
                    'lazylandscape_app.app()',
                    '\n'])
                    
    response = HttpResponse('')
    g = {
        "__builtins__" : __builtins__,
        "request" : request,
        "response" : response,
        "__name__" : __name__,
        "ShClasses" : ShClasses,
        }
        
    
    for i in cls.source():
        s = []
        #s.append('\ng = globals()\n')
        f, o = i[0],i[1]
        s.append('class %s:'%f)
        for v in  o:
            s.append(v['source'])
        #else:
            #for v in  o:
                #s.append(v['source'])
                
        cs = ''.join(s)
        print(cs)
        try:
            cx = compile(cs, '<%s>' % (f), 'exec')
            eval(cx,g)
        except SyntaxError as se:
            r = []
            r.append('<h2>SyntaxError</h2> <a href="#error_%d">%s</a> ' % (se.lineno, str(se)))
            c = 0
            for l in cs.splitlines():
                if c == se.lineno:
                    r.append('<div id="error_%d"><span style="background-color:red"> %d :</span><code>%s</code> </div>' % (c,c,escape(l)))
                else:
                    r.append('<div><span style="background-color:#aaa"> %d :</span><code>%s</code> </div>' % (c,escape(l)))
                c += 1
            return HttpResponse(''.join(r))
        
    appx = compile(app, '<App>', 'exec')
    eval(appx, g)
    return response
    
@csrf_exempt
def exec_(request, field, cls):
    try:
        cx = ShClasses.objects.filter(field=field).filter(name=cls)[0]
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
    
    