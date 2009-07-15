from django.conf.urls.defaults import *

from testproj.app import views

urlpatterns = patterns('',
    (r'^default/$', views.render_template),
    (r'^set_flash_var/$', views.set_flash_var),
    (r'^set_another_flash_var/$', views.set_another_flash_var),
    (r'^set_now_var/$', views.set_now_var),
    (r'^keep_var/$', views.keep_var),
    (r'^keep_var_decorator/$', views.keep_var_decorator),
    (r'^discard_var/$', views.discard_var),
    (r'^replace_flash/$', views.replace_flash),
    (r'^remove_flash/$', views.remove_flash),
)
