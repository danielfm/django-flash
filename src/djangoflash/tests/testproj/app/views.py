# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def render_template(request):
    return render_to_response('simple.html', {}, \
        context_instance=RequestContext(request))

def invalid_flash(request):
    request.flash = 'Something funny'
    return render_template(request)

def dict_syntax(request):
    request.flash['message'] = 'Oops'
    return render_template(request)

def flash_early_access(request):
    request.flash.put(message = 'Oops')
    return render_template(request)

def now(request):
    request.flash.now(message='Nice!')
    return render_template(request)

def variable_lifecycle(request):
    request.flash.put(message='Something funny')
    return render_template(request)

def several_variables_lifecycle(request):
    request.flash['another_message'] = 'Something else'
    return render_template(request)

def keep_variables(request):
    request.flash.keep('message')
    return render_template(request)

def keep_invalid_variables(request):
    request.flash.keep('something else')
    return render_template(request)

def keep_all_variables(request):
    request.flash.keep()
    return render_template(request)
