"""
Define views for ll.sh.get requests
"""

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import escape

import reversion
from sh.models import ShClasses



def source_(request, field, cls):
    try:
        cx = ShClasses.objects.filter(field=field).filter(name=cls)[0]
    except :
        raise Http404
    
    if cx.lang == 'python':
        s = []
        cxs = cx.source()
        for i in cxs:
            f, o = i[0],i[1]
            s.append('class %s:'%f)
            for v in  o:
                s.append(v['source'])

        return HttpResponse(''.join(s), content_type="text/plain")  
    elif cx.lang == 'js':
        return HttpResponse(cx.source(), content_type='application/javascript') 
        
    
    
def field_(request):
    """
    List fields
    """
    cx = ShClasses.objects.all()
    f = []
    for c in cx:
        if c.field not in f:
            f.append(c.field)
    return render_to_response("list_fields.html", {'fields' : f}, context_instance = RequestContext(request))

def class_(request, field):
    cx = ShClasses.objects.filter(field=field)
    return render_to_response("list_classes.html", {'clist' : cx, 'field' : field}, context_instance = RequestContext(request))
            
