# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from temper import get_temp as temp
from status_image import status_image

from models import Beer


def render_response(request, *args, **kwargs):
    if 'context_instance' not in kwargs:
        kwargs['context_instance'] = RequestContext(request)
    
    return render_to_response(*args, **kwargs)


def get_temp(request):
    return HttpResponse('%s' % temp(), mimetype="text/plain")


def index(request):
    beer_list = Beer.objects.filter(is_active=True)
    actual_temp = temp()
    
    return render_response(request, 'index.html', locals())

def status(request):
    beer_list = Beer.objects.filter(is_active=True)
    beer = beer_list[0] or None
    if beer:
        text = u'%s %s, T: %.1f ºC' % (_('Brewing'), beer.name, float(temp()))
    else:
        text = 'Currently not brewing.'
    
    response = HttpResponse(mimetype="image/png")
    status_image(text).save(response, 'PNG')
    return response