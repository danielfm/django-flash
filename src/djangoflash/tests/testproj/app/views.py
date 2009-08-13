# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from djangoflash.decorators import keep_messages


def render_template(request):
    return render_to_response('simple.html', \
        context_instance=RequestContext(request))

def set_flash_var(request):
    request.flash['message'] = 'Message'
    return render_template(request)

def set_another_flash_var(request):
    request.flash['anotherMessage'] = 'Another message'
    return render_template(request)

def set_now_var(request):
    request.flash.now['message'] = 'Message'
    return render_template(request)

def keep_var(request):
    request.flash.keep('message')
    return render_template(request)

@keep_messages('message')
def keep_var_decorator(request):
    return render_template(request)

def discard_var(request):
    # Should behave the same way 'flash.now' does
    request.flash['message'] = 'Message'
    request.flash.discard('message')
    return render_template(request)

def replace_flash(request):
    request.flash = "Replacing the flash with a string"
    return render_template(request)

def remove_flash(request):
    # I've seen this happen, I'm not kidding... :)
    del request.flash
    return render_template(request)
